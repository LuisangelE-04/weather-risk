# dict_keys(['lat', 'lon', 'timezone', 'timezone_offset', 'current', 'minutely', 'hourly', 'daily'])

def process_minutely_forecast(raw_forecast):
  '''
  rtype: return [] of minutely forecast
  '''
  return raw_forecast['minutely']

def process_hourly_forecast(raw_forecast):
  '''
  rtype: return [] of hourly forecast
  '''
  return raw_forecast['hourly']

def processs_daily_forecast(raw_forecast):
  '''
  rtype: return [] of daily forecast
  '''
  return raw_forecast['daily']
