import requests
from requests.adapters import HTTPAdapter, Retry
from ..config_loader import Config

cfg = Config()

HEADERS = {
  "User-Agent": cfg.user_agent,
  "accept": "application/geo+json"
}

session = requests.Session()
retries = Retry(
  total=cfg.retry_max,
  backoff_factor=cfg.retry_backoff,
  status_forcelist=(429, 500, 502, 503, 504)
)

session.mount("https://", HTTPAdapter(max_retries=retries))

def get_point(lat, lon):
  url = f"https://api.weather.gov/points/{lat},{lon}"
  req = session.get(url, headers=HEADERS, timeout=10)
  req.raise_for_status()
  return req.json()

def get_forecast(pointURL):
  url = pointURL
  req = session.get(url, headers=HEADERS, timeout=10)
  req.raise_for_status()
  return req.json()

def get_hourly_forecast(pointURL):
  url = pointURL
  req = session.get(url, headers=HEADERS, timeout=10)
  req.raise_for_status()
  return req.json()

def get_grid_data(pointURL):
  url = pointURL
  req = session.get(url, headers=HEADERS, timeout=10)
  req.raise_for_status()
  return req.json()

if __name__ == "__main__":
  lat = "29.8951"
  long = "-97.9093"
  point = get_point(lat, long)
  props = point["properties"]
  point_forecast = get_forecast(props['forecast'])
  propsf = point_forecast["properties"]["periods"]
  point_hourly_forecast = get_hourly_forecast(props['forecastHourly'])
  propsfh = point_hourly_forecast["properties"]["periods"]

  print(f"Resolved {lat},{long} -> {props['cwa']}, {props['gridId']}, {props['gridX']}, {props['gridY']}")

  print(f"Forecast URL: {props['forecast']}, Hourly Forecast URL: {props['forecastHourly']}, Grid Data URL: {props['forecastGridData']}")

  print(f"Forecase Daily: ")
  for period in propsf[:8]:
    print(f"{period['name']}, {period['probabilityOfPrecipitation']['value']}%, {period['temperature']}{period['temperatureUnit']}")
    print(f"{period['detailedForecast']}")

  grid_data = get_grid_data(props['forecastGridData'])
  keys = list(grid_data['properties'].keys())

  print(keys)

  '''
  print(f"Forecast Hourly: ")
  for period in propsfh[:8]:
    print(f"{period['startTime']}: {period['temperature']} {period['temperatureUnit']}, {period['shortForecast']}, Wind Speed: {period['windSpeed']} {period['windDirection']}")
  '''
