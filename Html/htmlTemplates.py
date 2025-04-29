import datetime

from Html.htmlGenerator import HtmlGenerator
from HomeAssistant.hassCommunicationsCoordinator import HassCommunicationsCoordinator
from utils.constants import *
from utils.logger import logger

class HtmlTemplates:
  def __init__(self):
    """
    Initializes the HtmlTemplates class.
    """
    self._h = HtmlGenerator()
    self._hassComms = HassCommunicationsCoordinator()

  
  def home(self):
    """
    Generates the HTML content for the home page of the dashboard.
    
    Returns:
      str: The HTML content for the home page.
    """
    return (
      self._h.html("", [
        self._h.head("", [
          self._h.link([f"rel='stylesheet' type='text/css' href={CSS_STYLESHEET_PATH}"]),
          self._h.meta(["name='viewport' content='width=device-width' initial-scale=1.0"]),
          self._h.meta([f"http-equiv='refresh' content={PAGE_REFRESH_INTERVAL_SECONDS}"]),
          self._h.title("", ["Dashboard"]),
        ]),

        self._h.body("", [
          self._h.table("border=2", [
            self._h.tr("", [
              self._h.td("", [self.get_time(time_type="currentTime")]),
              self._h.td("", [self.get_people_at_home()]),
            ]),
            self._h.tr("", [  
              self._h.td("id=big_table_cell", [
                self.weather_cell()
              ]),
              self._h.td("id=big_table_cell", [
                self.calendar_cell()
              ])
            ]),
            self._h.tr("", [
              self._h.td("colspan=2", [
                self.public_ip(),
                self._h.div("id=net_stats", [
                  self._h.p("", [self.display_double_net_stat(LAN_DOWNLOAD_SPD_SENSOR_ID, DOWNLOAD_SPD_SENSOR_ID, "Download", "arrow_down")]),
                  self._h.p("", [self.display_double_net_stat(LAN_UPLOAD_SPD_SENSOR_ID, UPLOAD_SPD_SENSOR_ID, "Upload", "arrow_up")]),
                ])
              ])
            ])
          ]),
        ])
      ]
      )
    )
  
  def title(self):
    """
    Generates an HTML <h1> element with the specified id and content.

    Returns:
      str: An HTML <h1> element with id "dash_title".
    """
    return self._h.h1("id=dash_title",["Lab Status"])
  
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
      temperature = weather['attributes']['temperature']
      dew_point = weather['attributes']['dew_point']
      condition = weather['state']

    return self._h.div("id=weather_cell", [
      self._h.p("id=city_name", [
        self._h.img(["id=city_icon", "src='../static/assets/weather_svg/location.svg'", "alt='city'"]),
        WEATHER_CITY_NAME,
        ]),
      self._h.p("id=temperature", [f"{temperature}&deg"]),
      self._h.img(["id=weather_icon", f"src='../static/assets/weather_svg/{condition}.svg'", f"alt='{condition}'"]),
      self._h.div("", [
        self._h.p("", [f"{self.weather_condition_formatter(condition)}"]),
        self._h.p("", [f"Dew Point: {dew_point}&deg"])
      ])
    ])
  
  def weather_condition_formatter(self, condition):
    """
    Formats a weather condition code into a human-readable string.
    
    Args:
      condition (str): The weather condition code to format.

    Returns:
      str: The formatted weather condition string. If the condition code is not recognized,
         returns "Format Err.".
    """
    condition_map = {
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
      "windy-variant": "Windy Variant"
    }
    return condition_map.get(condition, "Format Err.")

  def calendar_component(self):
    """
    Generates an HTML representation of the calendar component.
    This method retrieves the current date and formats it into a readable structure.

    Returns:
      str: An HTML string representing the calendar component.
    """
    [day, month, number] = datetime.datetime.now().strftime("%a %b %d").split()

    return self._h.div("id=date_field", [
      self._h.p("id=day_month", [f"{day}   {month}"]),
      self._h.p("id=date_number", [f"{int(number)}"])
    ])
  
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
      eta = int(float(resp['state']))

    return self._h.div("id=travel_time", [
      self._h.p("", [f"{eta} Minutes To Work"])
    ])

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

  def reload_button(self):
    """
    Generates an HTML button element that reloads the page when clicked.

    Returns:
      str: An HTML button element.
    """
    logger.info("Page reloaded from button")
    return self._h.button("onclick='location.reload()'", ["Reload"])

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

    return self._h.div("id=public_ip", [
      self._h.p("id=public_ip_addr", [f"Public IP: {ip}"])
    ])
  
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
      return -1.0
      
    return resp['state']
  
  def display_net_stat(self, entity_id, text, icon):
    """
    Generates an HTML representation of a single network statistic.
    This method retrieves the network statistic from a sensor and formats it.

    Args:
      entity_id (str): The sensor ID to retrieve the network statistic for.
      text (str): The text description of the network statistic.
      icon (str): The icon to display for the network statistic.

    Returns:
      str: An HTML string representing the network statistic.
    """
    stat = round(float(self.get_net_stat(entity_id)), 1)

    return self._h.div("id='net_stats_elem'", [
      self._h.p("", [
        self._h.img([f"id='net_icon' src='../static/assets/arrows/{icon}.svg' alt='{text}'"]),
        f'{stat}',
        " MB/S"
        ])
    ])
  
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

    stat_lan = round(float(self.get_net_stat(id_lan)), 1)
    stat_wan = round(float(self.get_net_stat(id_wan)), 1)
    
    return self._h.div("id='net_stats_elem'", [
      self._h.p("", [
        self._h.img([f"id='net_icon' src='../static/assets/arrows/{icon}.svg' alt='{text}'"]),
        f'{stat_lan}',
        " / ",
        f"{stat_wan}",
        " MB/S",
        ])
    ])

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
    if time_type== "lastUpdated":
      return self._h.h1("id='h1_time'", [f"Last Updated @{datetime.datetime.now().strftime('%H:%M')}"])
    elif time_type== "currentTime":
      return self._h.h1("id='h1_time'", [f"{datetime.datetime.now().strftime('%H:%M')}"])
    else:
      return f"Invalid time option: {time_type}"
    
  def get_people_at_home(self):
    """
    Generates an HTML header element indicating which people are currently at home.

    This method checks the presence of specific individuals using their tracker sensor IDs
    and returns an HTML <h1> element containing the initials of those who are at home.

    Returns:
      str: An HTML <h1> element with the initials of people at home.
        - 'C' for Claudio
        - 'F' for Federico
        - 'L' for Loretta
    """
    return self._h.h1("", [
      f"""@home: 
      {'C' if self.is_person_home(PERSON_1_TRACKER_SENSOR_ID) else ''}
      {"F" if self.is_person_home(PERSON_2_TRACKER_SENSOR_ID) else ''}
      {"L" if self.is_person_home(PERSON_3_TRACKER_SENSOR_ID) else ''}
      """
    ])
  
  def is_person_home(self, person_id):
      """
      Check if a person is home based on their personId.

      Args:
        person_id (str): The ID of the person to check.

      Returns:
        str: True if the person is home, otherwise False
      """
      resp = self._hassComms.getRequest(person_id)

      if resp["result"] != "OK":
        return False
      
      return True if resp["state"]=="home" else False

