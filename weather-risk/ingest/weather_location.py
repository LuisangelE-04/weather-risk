from .fetcher import (
  get_point, get_forecast, get_hourly_forecast, get_grid_data, get_openweather
)

from .processor import (
  process_minutely_forecast, process_hourly_forecast, processs_daily_forecast
)
from .risk_score import RiskScore

class WeatherLocation:
  def __init__(self, lat, lon, source='api', custom_data=None):
    self.lat = lat
    self.lon = lon

    self.point = get_point(lat, lon)
    self.props = self.point["properties"]
    self.grid_data = get_grid_data(self.props['forecastGridData'])
    self.daily_forecast = get_forecast(self.props['forecast'])
    self.hourly_forecast = get_hourly_forecast(self.props["forecastHourly"])

    if source == 'api':
      self.openweather_forecast = get_openweather(lat, lon)
    elif source == 'custom' and custom_data is not None:
      self.openweather_forecast = custom_data
    else:
      self.openweather_forecast = {"minutely": [], "hourly": [], "daily": []}

    self.processed_minutely = process_minutely_forecast(self.openweather_forecast)
    self.processed_hourly = process_hourly_forecast(self.openweather_forecast)
    self.processed_daily = processs_daily_forecast(self.openweather_forecast)
    self.risk_score = RiskScore(minutely_data=self.processed_minutely)

  def get_rain_risk(self):
    return self.risk_score.rain_risk_score()

  def print_processed(self):
    print(f"Minutely: {self.processed_minutely[:5]}\nHourly: {self.processed_hourly[:2]}\nDaily: {self.processed_daily[:2]}")
