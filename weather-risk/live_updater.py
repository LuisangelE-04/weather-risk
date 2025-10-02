import time
import json
from .ingest.weather_location import WeatherLocation
from .services.queue import push_to_queue
from .services.cache import cache_latest_risk
from .ingest.ingest_worker import save_risk_score
from .ingest.custom import get_custom_weather

LOCATIONS = [
  {"lat": 29.721345, "lon": -95.342013},
  {"lat": 29.758828, "lon": -95.370804}
]

loc_id = {29.721345 : 1, 29.758828 : 2}

with open("weather-risk/dataset/custom_minutely.json") as f:
  custom_data = json.load(f)

def live_update_generator():
  iteration = 0
  while True:
    payload = f"--- Update at {time.strftime('%Y-%m-%d %H:%M:%S')} ---"
    for loc in LOCATIONS:
      location_custom_data = get_custom_weather(loc["lat"], loc["lon"], iteration, custom_data)
      weather = WeatherLocation(
        loc["lat"], loc["lon"], 
        source='custom', 
        custom_data=location_custom_data
      )
      # weather = WeatherLocation(loc["lat"], loc["lon"])
      risk = weather.get_rain_risk()
      save_risk_score(loc_id[loc["lat"]], risk.get("risk_level"), risk, weather.processed_minutely)
      payload += f"\nLocation {loc['lat']},{loc['lon']}:\n{risk}\n"
      timestamp = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
      cache_latest_risk(loc["lat"], loc["lon"], risk, timestamp)

      event = {
        "lat": loc["lat"],
        "lon": loc["lon"],
        "risk": risk,
        "timestamp": timestamp
      }
      push_to_queue(json.dumps(event))

    yield payload
    iteration += 1
    time.sleep(600)

def get_latest_payload():
  payload = f"--- Update at {time.strftime('%Y-%m-%d %H:%M:%S')} ---"
  for loc in LOCATIONS:
    weather = WeatherLocation(loc["lat"], loc["lon"])
    risk = weather.get_rain_risk()
    payload += f"\nLocation {loc['lat']},{loc['lon']}:\n{risk}\n"
  return payload

if __name__ == "__main__":
  for payload in live_update_generator():
    print(payload)
    print("Waiting for next check...\n\n")