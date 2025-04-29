import requests

from utils.constants import *
from utils.logger import logger

class HassCommunicationsCoordinator:

  def __init__(self):
    self._address=f"""http://{HASS_IP}:{HASS_PORT}/api/"""
    self._headers = {
      'Content-Type': 'application/json',
      'Authorization': f'Bearer {HASS_TOKEN}'
    }

  def getRequest(self, id):
    response = requests.get(f"{self._address}states/{id}", headers=self._headers)
    response_json = response.json()

    if response.status_code != 200:
      logger.error(f"Error getting state for {id}: {response.status_code}")
      return {"result": "err"}
    
    if "message" in response_json and response_json["message"] == "Entity not found.":
      logger.error(f"This entity does not exist: {id}")
      return {"result": "err"}
    
    if "state" in response_json and response_json["state"] == "unavailable":
      logger.error(f"Unavailable entity w/ id: {id}")
      return {"result": "err"}
    
    response_json["result"] = "OK"
    return response_json