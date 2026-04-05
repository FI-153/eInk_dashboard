# Home Assistant Dashboard on eInk Displays
A simple Python server to display a basic HTML page optimized for eInk displays.

I wrote more about it [here](https://medium.com/@federicoimberti/repurposing-an-old-kobo-ereader-into-a-non-distracting-low-maintenance-home-assistant-dashboard-d04579a315b0).

![AnyConv com__e-ink-dash](https://github.com/user-attachments/assets/72790060-96a5-46ed-8d2f-29641c05c53d)

## Prerequisites

- Docker
- Docker Compose (V2)
- Python 3.9+ (for local development)

## Setup

1. Clone or download this repository
2. Copy `utils/constants.py.customize` to `utils/constants.py` and populate it with your Home Assistant instance's IP, port, token, and the name of the sensors you want to use

Sensor integrations used:
- For the weather I used [Met.no](https://www.home-assistant.io/integrations/met)
- For the ETA to work I used [Waze](https://www.home-assistant.io/integrations/waze_travel_time)
- The other sensors are custom helpers set up in HA that you can customize by reading the code

## Usage

### Docker (recommended)
```bash
make docker-up       # Build and start the container
make docker-down     # Stop the container
```

### Local Development
```bash
make setup           # Install dependencies
make run             # Start Flask dev server on 0.0.0.0:6123
```

### Tests & Linting
```bash
make test            # Run the test suite
make lint            # Check code style
make format          # Auto-fix lint issues and format code
```
