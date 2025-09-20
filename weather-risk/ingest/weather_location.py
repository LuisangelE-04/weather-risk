from .fetcher import (
  get_point, get_forecast, get_hourly_forecast, get_grid_data, get_openweather
)

from .processor import (
  process_minutely_forecast, process_hourly_forecast, processs_daily_forecast
)

class WeatherLocation:
  def __init__(self, lat, lon):
    self.lat = lat
    self.lon = lon
    self.point = get_point(lat, lon)
    self.props = self.point["properties"]
    self.grid_data = get_grid_data(self.props['forecastGridData'])
    self.daily_forecast = get_forecast(self.props['forecast'])
    self.hourly_forecast = get_hourly_forecast(self.props["forecastHourly"])
    self.openweather_forecast = get_openweather(lat, lon)
    self.processed_minutely = process_minutely_forecast(self.openweather_forecast)
    self.processed_hourly = process_hourly_forecast(self.openweather_forecast)
    self.processed_daily = processs_daily_forecast(self.openweather_forecast)

  def print_processed(self):
    print(f"Minutely: {self.processed_minutely[:5]}\nHourly: {self.processed_hourly[:2]}\nDaily: {self.processed_daily[:2]}")


if __name__ == "__main__":
  loc1 = WeatherLocation("29.721345", "-95.342013")
  loc2 = WeatherLocation("29.758828", "-95.370804")
  loc1.print_processed()
  loc2.print_processed()