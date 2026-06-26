import os

# Configuration is loaded from environment variables, populated locally from a
# .env file at the repository root and at runtime by Docker (see docker-compose.yml).

_ENV_PATH = os.path.join(os.path.dirname(__file__), "..", ".env")


# ponytail: minimal .env reader (flat KEY=VALUE, "#" comments, basic quote strip).
# Swap for python-dotenv only if values ever need multiline/escaping.
def _load_env(path=_ENV_PATH):
    if not os.path.exists(path):
        return
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            # setdefault: a real environment variable (e.g. from Docker) wins over .env
            os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


def _parse_person_trackers(raw):
    """
    Parses the PERSON_TRACKERS env var into a list of (entity_id, label) pairs.

    Args:
      raw (str): Comma-separated "entity_id:label" entries (e.g. "person.a:A,person.b:B").

    Returns:
      list: (entity_id, label) tuples; empty or malformed entries are skipped.
    """
    trackers = []
    for entry in raw.split(","):
        entity_id, sep, label = entry.partition(":")
        entity_id, label = entity_id.strip(), label.strip()
        if entity_id and sep:
            trackers.append((entity_id, label))
    return trackers


# Only load the .env file for local debugging (`make debug` sets USE_DOTENV=1).
# Docker and other deployments pass configuration as real environment variables.
if os.getenv("USE_DOTENV") == "1":
    _load_env()

HASS_IP = os.getenv("HASS_IP", "")
HASS_PORT = os.getenv("HASS_PORT", "")
HASS_TOKEN = os.getenv("HASS_TOKEN", "")

PAGE_REFRESH_INTERVAL_SECONDS = int(os.getenv("PAGE_REFRESH_INTERVAL_SECONDS") or "60")

CSS_STYLESHEET_PATH = os.getenv("CSS_STYLESHEET_PATH", "./static/css/styles.css")

WEATHER_SENSOR_ID = os.getenv("WEATHER_SENSOR_ID", "")
WEATHER_CITY_NAME = os.getenv("WEATHER_CITY_NAME", "")
ETA_TO_WORK_SENSOR_ID = os.getenv("ETA_TO_WORK_SENSOR_ID", "")
PUBLIC_IP_SENSOR_ID = os.getenv("PUBLIC_IP_SENSOR_ID", "")
DOWNLOAD_SPD_SENSOR_ID = os.getenv("DOWNLOAD_SPD_SENSOR_ID", "")
UPLOAD_SPD_SENSOR_ID = os.getenv("UPLOAD_SPD_SENSOR_ID", "")
LAN_DOWNLOAD_SPD_SENSOR_ID = os.getenv("LAN_DOWNLOAD_SPD_SENSOR_ID", "")
LAN_UPLOAD_SPD_SENSOR_ID = os.getenv("LAN_UPLOAD_SPD_SENSOR_ID", "")

# Comma-separated "entity_id:label" pairs shown in the "@home" section.
PERSON_TRACKERS = _parse_person_trackers(os.getenv("PERSON_TRACKERS", ""))
