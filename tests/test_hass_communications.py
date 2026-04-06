from unittest.mock import MagicMock, patch

import requests

from HomeAssistant.hassCommunicationsCoordinator import HassCommunicationsCoordinator


class TestHassCommunicationsCoordinator:
    def setup_method(self):
        with (
            patch("HomeAssistant.hassCommunicationsCoordinator.HASS_IP", "192.168.1.1"),
            patch("HomeAssistant.hassCommunicationsCoordinator.HASS_PORT", "8123"),
            patch("HomeAssistant.hassCommunicationsCoordinator.HASS_TOKEN", "test-token"),
        ):
            self.coordinator = HassCommunicationsCoordinator()

    @patch("HomeAssistant.hassCommunicationsCoordinator.requests.get")
    def test_successful_request(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"state": "sunny", "attributes": {"temperature": 22}}
        mock_get.return_value = mock_response

        result = self.coordinator.getRequest("sensor.weather")

        assert result["result"] == "OK"
        assert result["state"] == "sunny"
        assert result["attributes"]["temperature"] == 22
        mock_get.assert_called_once()

    @patch("HomeAssistant.hassCommunicationsCoordinator.requests.get")
    def test_non_200_status_code(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.json.return_value = {}
        mock_get.return_value = mock_response

        result = self.coordinator.getRequest("sensor.weather")

        assert result["result"] == "err"

    @patch("HomeAssistant.hassCommunicationsCoordinator.requests.get")
    def test_entity_not_found(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"message": "Entity not found."}
        mock_get.return_value = mock_response

        result = self.coordinator.getRequest("sensor.nonexistent")

        assert result["result"] == "err"

    @patch("HomeAssistant.hassCommunicationsCoordinator.requests.get")
    def test_unavailable_entity(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"state": "unavailable"}
        mock_get.return_value = mock_response

        result = self.coordinator.getRequest("sensor.offline")

        assert result["result"] == "err"

    @patch("HomeAssistant.hassCommunicationsCoordinator.requests.get")
    def test_request_includes_auth_header(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"state": "on"}
        mock_get.return_value = mock_response

        self.coordinator.getRequest("sensor.test")

        headers = mock_get.call_args.kwargs["headers"]
        assert "Bearer test-token" in headers["Authorization"]

    @patch("HomeAssistant.hassCommunicationsCoordinator.requests.get")
    def test_request_url_format(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"state": "on"}
        mock_get.return_value = mock_response

        self.coordinator.getRequest("sensor.my_sensor")

        call_args = mock_get.call_args[0][0]
        assert call_args == "http://192.168.1.1:8123/api/states/sensor.my_sensor"

    @patch("HomeAssistant.hassCommunicationsCoordinator.requests.get")
    def test_is_reachable_returns_true_when_api_healthy(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        assert self.coordinator.isReachable() is True
        mock_get.assert_called_once_with(
            "http://192.168.1.1:8123/api/",
            headers=self.coordinator._headers,
            timeout=5,
        )

    @patch("HomeAssistant.hassCommunicationsCoordinator.requests.get")
    def test_is_reachable_returns_false_on_non_200(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 503
        mock_get.return_value = mock_response

        assert self.coordinator.isReachable() is False

    @patch("HomeAssistant.hassCommunicationsCoordinator.requests.get")
    def test_is_reachable_returns_false_on_connection_error(self, mock_get):
        mock_get.side_effect = requests.ConnectionError()

        assert self.coordinator.isReachable() is False

    @patch("HomeAssistant.hassCommunicationsCoordinator.requests.get")
    def test_is_reachable_returns_false_on_timeout(self, mock_get):
        mock_get.side_effect = requests.Timeout()

        assert self.coordinator.isReachable() is False

    @patch("HomeAssistant.hassCommunicationsCoordinator.requests.get")
    def test_get_request_returns_err_on_connection_error(self, mock_get):
        mock_get.side_effect = requests.ConnectionError()

        result = self.coordinator.getRequest("sensor.weather")

        assert result["result"] == "err"
