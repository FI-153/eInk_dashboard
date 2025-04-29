# Home Assistant Dashboard on eInk Displays
The following is the code i wrote to display the dashboard i wrote about in [this](https://medium.com/@federicoimberti/repurposing-an-old-kobo-ereader-into-a-non-distracting-low-maintenance-home-assistant-dashboard-d04579a315b0) article.

## Deployment
You can deploy via Docker

`sudo docker run .`

and Docker Compose

`sudo docker compose up -d`

### Before Lunching
Rename the file `utils/constants.py.customize` to `utils/constants.py` and populate it with your instance's IP, port, token and the name of the sensors you want to use. For the weather i used [Met.no](https://www.home-assistant.io/integrations/met) and [Waze](https://www.home-assistant.io/integrations/waze_travel_time) for the ETA to work. The other sensors are custom templates based on my setup which you can tailor to your own by reading the code.

### Requisites
Install them as you prefer:
- docker
- docker-compose
