from unittest.mock import MagicMock, patch

from Html.htmlTemplates import HtmlTemplates
from utils.constants import CSS_STYLESHEET_PATH, PAGE_REFRESH_INTERVAL_SECONDS


def _make_ok(state, attributes=None):
    resp = {"state": state, "result": "OK"}
    if attributes:
        resp["attributes"] = attributes
    return resp


ERR_RESPONSE = {"result": "err"}


def _make_templates():
    """Create HtmlTemplates with a mocked HassCommunicationsCoordinator."""
    with patch("Html.htmlTemplates.HassCommunicationsCoordinator"):
        templates = HtmlTemplates()
    return templates


class TestWeatherConditionFormatter:
    def setup_method(self):
        self.templates = _make_templates()

    def test_known_conditions(self):
        assert self.templates.weather_condition_formatter("sunny") == "Sunny"
        assert self.templates.weather_condition_formatter("cloudy") == "Cloudy"
        assert self.templates.weather_condition_formatter("rainy") == "Rainy"
        assert self.templates.weather_condition_formatter("partlycloudy") == "Partly Cloudy"
        assert self.templates.weather_condition_formatter("clear-night") == "Clear Night"
        assert self.templates.weather_condition_formatter("lightning-rainy") == "Lightning with Rain"

    def test_unknown_condition(self):
        assert self.templates.weather_condition_formatter("unknown") == "Format Err."


class TestWeatherCell:
    def setup_method(self):
        self.templates = _make_templates()
        self.mock_comms = self.templates._hassComms

    def test_weather_cell_success(self):
        self.mock_comms.getRequest.return_value = _make_ok("sunny", {"temperature": 25, "dew_point": 15})
        result = self.templates.weather_cell()
        assert "25" in result
        assert "15" in result
        assert "sunny" in result

    def test_weather_cell_error(self):
        self.mock_comms.getRequest.return_value = ERR_RESPONSE
        result = self.templates.weather_cell()
        assert "Err" in result


class TestCalendarComponent:
    def setup_method(self):
        self.templates = _make_templates()

    @patch("Html.htmlTemplates.datetime")
    def test_calendar_component(self, mock_datetime):
        mock_now = MagicMock()
        mock_now.strftime.return_value = "Mon Apr 05"
        mock_datetime.datetime.now.return_value = mock_now
        result = self.templates.calendar_component()
        assert "Mon" in result
        assert "Apr" in result
        assert "5" in result


class TestEtaToWork:
    def setup_method(self):
        self.templates = _make_templates()
        self.mock_comms = self.templates._hassComms

    def test_eta_success(self):
        self.mock_comms.getRequest.return_value = _make_ok("23.5")
        result = self.templates.eta_to_work_component()
        assert "23" in result
        assert "Minutes To Work" in result

    def test_eta_error(self):
        self.mock_comms.getRequest.return_value = ERR_RESPONSE
        result = self.templates.eta_to_work_component()
        assert "Err" in result


class TestPublicIp:
    def setup_method(self):
        self.templates = _make_templates()
        self.mock_comms = self.templates._hassComms

    def test_public_ip_success(self):
        self.mock_comms.getRequest.return_value = _make_ok("203.0.113.1")
        result = self.templates.public_ip()
        assert "203.0.113.1" in result

    def test_public_ip_error(self):
        self.mock_comms.getRequest.return_value = ERR_RESPONSE
        result = self.templates.public_ip()
        assert "Err" in result


class TestNetStats:
    def setup_method(self):
        self.templates = _make_templates()
        self.mock_comms = self.templates._hassComms

    def test_get_net_stat_success(self):
        self.mock_comms.getRequest.return_value = _make_ok("95.5")
        result = self.templates.get_net_stat("sensor.download")
        assert result == "95.5"

    def test_get_net_stat_error(self):
        self.mock_comms.getRequest.return_value = ERR_RESPONSE
        result = self.templates.get_net_stat("sensor.download")
        assert result == -1.0

    def test_display_double_net_stat(self):
        self.mock_comms.getRequest.side_effect = [
            _make_ok("100.5"),
            _make_ok("50.3"),
        ]
        result = self.templates.display_double_net_stat("sensor.lan_dl", "sensor.wan_dl", "Download", "arrow_down")
        assert "100.5" in result
        assert "50.3" in result
        assert "MB/S" in result


class TestGetTime:
    def setup_method(self):
        self.templates = _make_templates()

    @patch("Html.htmlTemplates.datetime")
    def test_current_time(self, mock_datetime):
        mock_now = MagicMock()
        mock_now.strftime.return_value = "14:30"
        mock_datetime.datetime.now.return_value = mock_now
        result = self.templates.get_time(time_type="currentTime")
        assert "14:30" in result

    @patch("Html.htmlTemplates.datetime")
    def test_last_updated(self, mock_datetime):
        mock_now = MagicMock()
        mock_now.strftime.return_value = "14:30"
        mock_datetime.datetime.now.return_value = mock_now
        result = self.templates.get_time(time_type="lastUpdated")
        assert "Last Updated" in result
        assert "14:30" in result

    def test_invalid_time_type(self):
        result = self.templates.get_time(time_type="invalid")
        assert "Invalid time option" in result


class TestPeopleAtHome:
    def setup_method(self):
        self.templates = _make_templates()
        self.mock_comms = self.templates._hassComms

    def test_person_home(self):
        self.mock_comms.getRequest.return_value = _make_ok("home")
        assert self.templates.is_person_home("person.test") is True

    def test_person_away(self):
        self.mock_comms.getRequest.return_value = _make_ok("not_home")
        assert self.templates.is_person_home("person.test") is False

    def test_person_error(self):
        self.mock_comms.getRequest.return_value = ERR_RESPONSE
        assert self.templates.is_person_home("person.test") is False


class TestBuildHead:
    def setup_method(self):
        self.templates = _make_templates()

    def test_meta_refresh_content_value_is_quoted(self):
        # Old e-reader browsers fail to honor http-equiv refresh when the
        # content value is unquoted (e.g. content=60), so it must be quoted.
        result = self.templates._build_head()
        assert f"content='{PAGE_REFRESH_INTERVAL_SECONDS}'" in result
        assert f"content={PAGE_REFRESH_INTERVAL_SECONDS}>" not in result

    def test_viewport_initial_scale_inside_content_attribute(self):
        # initial-scale must live inside the viewport content attribute, not
        # leak out as a malformed standalone attribute.
        result = self.templates._build_head()
        assert "content='width=device-width, initial-scale=1.0'" in result
        assert "content='width=device-width' initial-scale=1.0" not in result

    def test_stylesheet_href_value_is_quoted(self):
        # Old e-reader browsers can fail to load attributes whose values are
        # unquoted (e.g. href=./styles.css), so the stylesheet href must be
        # quoted just like the meta tags.
        result = self.templates._build_head()
        assert f"href='{CSS_STYLESHEET_PATH}'" in result
        assert f"href={CSS_STYLESHEET_PATH}" not in result


class TestOfflinePage:
    def setup_method(self):
        self.templates = _make_templates()

    def test_offline_page_contains_offline_message(self):
        result = self.templates.offline_page()
        assert "Home Assistant is Offline" in result

    @patch("Html.htmlTemplates.datetime")
    def test_offline_page_contains_current_time(self, mock_datetime):
        mock_now = MagicMock()
        mock_now.strftime.return_value = "14:30"
        mock_datetime.datetime.now.return_value = mock_now
        result = self.templates.offline_page()
        assert "14:30" in result

    def test_offline_page_contains_meta_refresh(self):
        result = self.templates.offline_page()
        assert "http-equiv='refresh'" in result

    def test_offline_page_contains_stylesheet(self):
        result = self.templates.offline_page()
        assert "stylesheet" in result

    def test_offline_page_has_offline_message_id(self):
        result = self.templates.offline_page()
        assert "offline_message" in result


class TestHomeBranching:
    def setup_method(self):
        self.templates = _make_templates()
        self.mock_comms = self.templates._hassComms

    def test_home_returns_offline_page_when_unreachable(self):
        self.mock_comms.isReachable.return_value = False
        result = self.templates.home()
        assert "Home Assistant is Offline" in result

    def test_home_returns_dashboard_when_reachable(self):
        self.mock_comms.isReachable.return_value = True
        self.mock_comms.getRequest.return_value = _make_ok("10.0", {"temperature": 25, "dew_point": 15})
        result = self.templates.home()
        assert "Home Assistant is Offline" not in result
        assert "table" in result
