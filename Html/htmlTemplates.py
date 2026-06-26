import datetime

from HomeAssistant.hassCommunicationsCoordinator import HassCommunicationsCoordinator
from Html.htmlGenerator import HtmlGenerator
from utils.constants import *

WEATHER_CONDITION_MAP = {
    "clear-night": "Clear Night",
    "cloudy": "Cloudy",
    "fog": "Foggy",
    "hail": "Hailing",
    "lightning": "Lightning",
    "lightning-rainy": "Lightning with Rain",
    "partlycloudy": "Partly Cloudy",
    "pouring": "Pouring",
    "rainy": "Rainy",
    "snowy": "Snowy",
    "snowy-rainy": "Snow with Rain",
    "sunny": "Sunny",
    "windy": "Windy",
    "windy-variant": "Windy Variant",
}


class HtmlTemplates:
    def __init__(self):
        """
        Initializes the HtmlTemplates class.
        """
        self._h = HtmlGenerator()
        self._hassComms = HassCommunicationsCoordinator()

    def _build_head(self):
        """
        Builds the standard HTML <head> section shared by all pages.

        Returns:
          str: The HTML <head> element with stylesheet, viewport, meta-refresh, and title.
        """
        return self._h.head(
            "",
            [
                self._h.link(["rel='stylesheet'", "type='text/css'", f"href='{CSS_STYLESHEET_PATH}'"]),
                self._h.meta(["name='viewport'", "content='width=device-width, initial-scale=1.0'"]),
                self._h.meta(["http-equiv='refresh'", f"content='{PAGE_REFRESH_INTERVAL_SECONDS}'"]),
                self._h.title("", ["Dashboard"]),
            ],
        )

    def home(self):
        """
        Generates the HTML content for the home page of the dashboard.

        Returns:
          str: The HTML content for the home page.
        """
        if not self._hassComms.isReachable():
            return self.offline_page()

        return self.dashboard()

    def dashboard(self) -> str:
        """
        Generates an HTML page for the main dashboard.

        Returns:
          str: The HTML content for the dashboard page.
        """

        return self._h.html(
            "",
            [
                self._build_head(),
                self._h.body(
                    "",
                    [
                        self._h.table(
                            "border=2",
                            [
                                self._h.tr(
                                    "",
                                    [
                                        self._h.td("", [self.get_time(time_type="currentTime")]),
                                        self._h.td("", [self.get_people_at_home()]),
                                    ],
                                ),
                                self._h.tr(
                                    "",
                                    [
                                        self._h.td("id=big_table_cell", [self.weather_cell()]),
                                        self._h.td("id=big_table_cell", [self.calendar_cell()]),
                                    ],
                                ),
                                self._h.tr(
                                    "",
                                    [
                                        self._h.td(
                                            "colspan=2",
                                            [
                                                self.public_ip(),
                                                self._h.div(
                                                    "id=net_stats",
                                                    [
                                                        self._h.p(
                                                            "",
                                                            [
                                                                self.display_double_net_stat(
                                                                    LAN_DOWNLOAD_SPD_SENSOR_ID,
                                                                    DOWNLOAD_SPD_SENSOR_ID,
                                                                    "Download",
                                                                    "arrow_down",
                                                                )
                                                            ],
                                                        ),
                                                        self._h.p(
                                                            "",
                                                            [
                                                                self.display_double_net_stat(
                                                                    LAN_UPLOAD_SPD_SENSOR_ID,
                                                                    UPLOAD_SPD_SENSOR_ID,
                                                                    "Upload",
                                                                    "arrow_up",
                                                                )
                                                            ],
                                                        ),
                                                    ],
                                                ),
                                            ],
                                        )
                                    ],
                                ),
                            ],
                        ),
                    ],
                ),
            ],
        )

    def offline_page(self) -> str:
        """
        Generates an HTML page indicating Home Assistant is offline.

        Displays a centered "Home Assistant is Offline" message with the
        current time below it. Includes meta-refresh so the page will
        automatically recover when Home Assistant comes back online.

        Returns:
          str: The HTML content for the offline page.
        """
        return self._h.html(
            "",
            [
                self._build_head(),
                self._h.body(
                    "",
                    [
                        self._h.div(
                            "id=offline_wrapper",
                            [
                                self._h.div(
                                    "id=offline_message",
                                    [
                                        self._h.h1("", ["Home Assistant is Offline"]),
                                        self._h.p("", [f"{datetime.datetime.now().strftime('%H:%M')}"]),
                                    ],
                                ),
                            ],
                        ),
                    ],
                ),
            ],
        )

    def weather_cell(self):
        """
        Generates an HTML representation of the weather cell.
        This method retrieves weather data from a sensor, formats it, and returns
        an HTML structure displaying the weather information including temperature,
        dew point, and condition.
        The HTML structure includes:
          - City name with an icon.
          - Temperature.
          - Weather condition icon.
          - Weather condition description.
          - Dew point.

        If the weather data is not available, it displays "Err" for temperature,
        dew point, and condition.

        Returns:
          str: An HTML string representing the weather cell.
        """
        weather = self._hassComms.getRequest(WEATHER_SENSOR_ID)

        if weather["result"] != "OK":
            [temperature, dew_point, condition] = ["Err", "Err", "Err"]
        else:
            attributes = weather.get("attributes", {})
            temperature = attributes.get("temperature", "Err")
            dew_point = attributes.get("dew_point", "Err")
            condition = weather.get("state", "Err")

        return self._h.div(
            "id=weather_cell",
            [
                self._h.p(
                    "id=city_name",
                    [
                        self._h.img(["id=city_icon", "src='../static/assets/weather_svg/location.svg'", "alt='city'"]),
                        WEATHER_CITY_NAME,
                    ],
                ),
                self._h.p("id=temperature", [f"{temperature}&deg"]),
                self._h.img(
                    ["id=weather_icon", f"src='../static/assets/weather_svg/{condition}.svg'", f"alt='{condition}'"]
                ),
                self._h.div(
                    "",
                    [
                        self._h.p("", [f"{self.weather_condition_formatter(condition)}"]),
                        self._h.p("", [f"Dew Point: {dew_point}&deg"]),
                    ],
                ),
            ],
        )

    def weather_condition_formatter(self, condition):
        """
        Formats a weather condition code into a human-readable string.

        Args:
          condition (str): The weather condition code to format.

        Returns:
          str: The formatted weather condition string. If the condition code is not recognized,
             returns "Format Err.".
        """
        return WEATHER_CONDITION_MAP.get(condition, "Format Err.")

    def calendar_component(self):
        """
        Generates an HTML representation of the calendar component.
        This method retrieves the current date and formats it into a readable structure.

        Returns:
          str: An HTML string representing the calendar component.
        """
        [day, month, number] = datetime.datetime.now().strftime("%a %b %d").split()

        return self._h.div(
            "id=date_field",
            [self._h.p("id=day_month", [f"{day}   {month}"]), self._h.p("id=date_number", [f"{int(number)}"])],
        )

    def eta_to_work_component(self):
        """
        Generates an HTML representation of the ETA to work component.
        This method retrieves the estimated time of arrival to work from a sensor and formats it.

        Returns:
          str: An HTML string representing the ETA to work component.
        """
        resp = self._hassComms.getRequest(ETA_TO_WORK_SENSOR_ID)

        if resp["result"] != "OK":
            eta = "Err"
        else:
            eta = int(float(resp["state"]))

        return self._h.div("id=travel_time", [self._h.p("", [f"{eta} Minutes To Work"])])

    def calendar_cell(self):
        """
        Generates an HTML representation of the calendar cell.
        This method combines the calendar component and ETA to work component into a single cell.

        Returns:
          str: An HTML string representing the calendar cell.
        """
        return f"""
            {self.calendar_component()}
            {self.eta_to_work_component()}
          """

    def public_ip(self):
        """
        Generates an HTML representation of the public IP address.
        This method retrieves the public IP address from a sensor and formats it.

        Returns:
          str: An HTML string representing the public IP address.
        """
        resp = self._hassComms.getRequest(PUBLIC_IP_SENSOR_ID)

        if resp["result"] != "OK":
            ip = "Err"
        else:
            ip = resp["state"]

        return self._h.div("id=public_ip", [self._h.p("id=public_ip_addr", [f"Public IP: {ip}"])])

    def get_net_stat(self, entity_id):
        """
        Retrieves the network statistic for the given sensor ID.

        Args:
          entity_id (str): The sensor ID to retrieve the network statistic for.

        Returns:
          str: The network statistic value as a string. Returns "Err" if the data is not available.
        """
        resp = self._hassComms.getRequest(entity_id)

        if resp["result"] != "OK":
            return "Err"

        return resp["state"]

    def _format_net_stat(self, value):
        """
        Formats a network statistic value for display.

        Args:
          value: The raw network statistic value (a numeric string or "Err").

        Returns:
          The value rounded to one decimal place, or "Err" if it is not numeric.
        """
        try:
            return round(float(value), 1)
        except (ValueError, TypeError):
            return "Err"

    def display_double_net_stat(self, id_lan, id_wan, text, icon):
        """
        Generates an HTML representation of two network statistics (LAN and WAN).
        This method retrieves the network statistics from sensors and formats them.

        Args:
          id_lan (str): The sensor ID to retrieve the LAN network statistic for.
          id_wan (str): The sensor ID to retrieve the WAN network statistic for.
          text (str): The text to the right of the network statistic.
          icon (str): The icon to display on the left for the network statistic.

        Returns:
          str: An HTML string representing the LAN and WAN network statistics.
        """

        stat_lan = self._format_net_stat(self.get_net_stat(id_lan))
        stat_wan = self._format_net_stat(self.get_net_stat(id_wan))

        return self._h.div(
            "id='net_stats_elem'",
            [
                self._h.p(
                    "",
                    [
                        self._h.img([f"id='net_icon' src='../static/assets/arrows/{icon}.svg' alt='{text}'"]),
                        f"{stat_lan}",
                        " / ",
                        f"{stat_wan}",
                        " MB/S",
                    ],
                )
            ],
        )

    def get_time(self, time_type="lastUpdated"):
        """
        Generates an HTML <h1> element displaying the specified time.

        Args:
          time_type (str): The type of time to display. Options are "lastUpdated" for the last update time
                and "currentTime" for the current time. Defaults to "lastUpdated". In order to have a
                correctly updated time you must set PAGE_REFRESH_INTERVAL_SECONDS to 60 seconds.
                Otherwise if you can run scripts just call this method once every minute.

        Returns
          str: An HTML <h1> element with the specified time or an error message if the type is invalid.
        """
        if time_type == "lastUpdated":
            return self._h.h1("id='h1_time'", [f"Last Updated @{datetime.datetime.now().strftime('%H:%M')}"])
        elif time_type == "currentTime":
            return self._h.h1("id='h1_time'", [f"{datetime.datetime.now().strftime('%H:%M')}"])
        else:
            return f"Invalid time option: {time_type}"

    def get_people_at_home(self):
        """
        Generates an HTML header element indicating which people are currently at home.

        Iterates over PERSON_TRACKERS, a list of (entity_id, label) pairs, and renders the
        label of each person whose tracker reports them as home. Entries whose ID is unset
        or unreachable are simply skipped, so the section adapts to any number of configured
        people without crashing on partial configuration.

        Returns:
          str: An HTML <h1> element with the labels of people at home.
        """
        initials = "".join(f" {label}" for entity_id, label in PERSON_TRACKERS if self.is_person_home(entity_id))
        return self._h.h1("", [f"@home:{initials}"])

    def is_person_home(self, person_id):
        """
        Check if a person is home based on their personId.

        Args:
          person_id (str): The ID of the person to check.

        Returns:
          bool: True if the person is home, otherwise False.
        """
        resp = self._hassComms.getRequest(person_id)

        if resp["result"] != "OK":
            return False

        return resp["state"] == "home"
