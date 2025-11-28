# Home Assistant Dashboard on eInk Displays
A simple python server to display a basic HTML page optimized for eInk displays.

I wrote more about it [here](https://medium.com/@federicoimberti/repurposing-an-old-kobo-ereader-into-a-non-distracting-low-maintenance-home-assistant-dashboard-d04579a315b0).

![AnyConv com__e-ink-dash](https://github.com/user-attachments/assets/72790060-96a5-46ed-8d2f-29641c05c53d)

## Usage
Clone or download this repository, navigate to its root then deploy the server via **Docker**
```bash
sudo docker run .
```
Or **Docker Compose**
```bash
sudo docker compose up -d
```

### Before Launching
Rename the file `utils/constants.py.customize` to `utils/constants.py` and populate it with your instance's IP, port, token and the name of the sensors you want to use. 

- For the weather i used [Met.no](https://www.home-assistant.io/integrations/met);

- For the ETA to work i used [Waze](https://www.home-assistant.io/integrations/waze_travel_time);

- The other sensors are custom helpers setup in HA that you can customize based on my setup which you can tailor to your own by reading the code.

### Requisites
Install them as you prefer:
- docker
- docker-compose
