import os
import requests
from requests.adapters import HTTPAdapter, Retry
from ..config_loader import Config
from dotenv import load_dotenv

cfg = Config()
load_dotenv()

openweather_source = next((ds for ds in cfg.data_sources if ds["name"] == "openweather"), {})
openweather_api_key = os.getenv("OPENWEATHER_API_KEY")
openweather_base_url = openweather_source.get("base_url")
weather_gov_source = next((ds for ds in cfg.data_sources if ds["name"] == "weather_gov"), {})
user_agent = weather_gov_source.get("user_agent")

HEADERS = {
  "User-Agent": user_agent,
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

def get_openweather(lat, lon):
  if not openweather_api_key or not openweather_base_url:
    raise ValueError("OpenWeather API key or base URL not configured")
  
  url = f"{openweather_base_url}&appid={openweather_api_key}&lat={lat}&lon={lon}"
  req = session.get(url, timeout=10)
  req.raise_for_status()
  return req.json()
