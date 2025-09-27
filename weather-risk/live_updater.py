import time
import json
from .ingest.weather_location import WeatherLocation
from .services.queue import push_to_queue
from .services.cache import cache_latest_risk

LOCATIONS = [
  {"lat": 29.721345, "lon": -95.342013},
  {"lat": 29.758828, "lon": -95.370804}
]


def live_update_generator():
  while True:
    payload = f"--- Update at {time.strftime('%Y-%m-%d %H:%M:%S')} ---"
    for loc in LOCATIONS:
      weather = WeatherLocation(loc["lat"], loc["lon"])
      risk = weather.get_rain_risk()
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
    time.sleep(20)

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