def get_custom_weather(lat, lon, iteration, custom_data):
  '''
  fetch iteration based on the location and iteration

  rtype: return {} as raw data
  '''
  key = f"{lat},{lon}"
  location_data = custom_data.get(key, [])
  
  if iteration < len(location_data):
    return location_data[iteration]
  else:
    return None
  