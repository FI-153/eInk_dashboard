import requests

from utils.constants import *
from utils.logger import logger


class HassCommunicationsCoordinator:
    def __init__(self):
        self._address = f"""http://{HASS_IP}:{HASS_PORT}/api/"""
        self._headers = {"Content-Type": "application/json", "Authorization": f"Bearer {HASS_TOKEN}"}

    def isReachable(self):
        """
        Checks if the Home Assistant API is reachable.

        Sends a GET request to the API root with a 5-second timeout.

        Returns:
          bool: True if the API responds with status 200, False otherwise.
        """
        try:
            response = requests.get(
                self._address,
                headers=self._headers,
                timeout=5,
            )
            if response.status_code != 200:
                logger.error(f"HA API returned status {response.status_code}")
            return response.status_code == 200
        except requests.RequestException as e:
            logger.error(f"HA API unreachable: {e}")
            return False

    def getRequest(self, id):
        """
        Fetches the state of a Home Assistant entity by ID.

        Args:
          id (str): The entity ID to fetch.

        Returns:
          dict: The entity state as a dict with a "result" key set to "OK" on success
              or "err" on failure.
        """
        try:
            response = requests.get(f"{self._address}states/{id}", headers=self._headers, timeout=5)
        except requests.RequestException:
            logger.error(f"Connection failed for {id}")
            return {"result": "err"}

        if response.status_code != 200:
            logger.error(f"Error getting state for {id}: {response.status_code}")
            return {"result": "err"}

        try:
            response_json = response.json()
        except ValueError:
            logger.error(f"Non-JSON response for {id}")
            return {"result": "err"}

        if "message" in response_json and response_json["message"] == "Entity not found.":
            logger.error(f"This entity does not exist: {id}")
            return {"result": "err"}

        if response_json.get("state") in ("unavailable", "unknown", None):
            logger.error(f"Unavailable entity w/ id: {id}")
            return {"result": "err"}

        response_json["result"] = "OK"
        return response_json
