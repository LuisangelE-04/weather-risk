import time
from .ingest.weather_location import WeatherLocation

LOCATIONS = [
  {"lat": 29.721345, "lon": -95.342013},
  {"lat": 29.758828, "lon": -95.370804}
]

def run_live_update():
  while True:
    print(f"--- Update at {time.strftime('%Y-%m-%d %H:%M:%S')} ---")
    
    for loc in LOCATIONS:
      weather = WeatherLocation(loc["lat"], loc["lon"])
      risk = weather.get_rain_risk()
      print(f"Location {loc['lat']},{loc['lon']}:\n{risk}\n")

    print("Waiting for next check...\n\n")
    time.sleep(5)

if __name__ == "__main__":
  run_live_update()