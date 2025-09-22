class RiskScore:
  def __init__(self, minutely_data=None, hourly_data=None, daily_data=None):
    self.minutely_data = minutely_data or []
    self.hourly_data = hourly_data or []
    self.daily_data = daily_data or []

  def get_window(self, start, end):
    return self.minutely_data[start:end]

  def has_persistent_rain(self, window, threshold, window_size):
    for i in range(len(window) - window_size + 1):
      group = window[i:i + window_size]
      
      if all(item.get('precipitation', 0) > threshold for item in group):
        return True
    return False
  
  def has_spike(self, window, threshold):
    for i in range(1, len(window) - 1):
      if (window[i-1].get('precipitation', 0) <= threshold and
          window[i].get('precipitation', 0) > threshold and
          window[i+1].get('precipitation', 0) <= threshold):
        return True
      return False
    
  def max_window_sum_avg(self, window, window_size):
    max_sum = 0
    max_avg = 0

    for i in range(len(window) - window_size + 1):
      group = window[i:i + window_size]
      vals = [item.get('precipitation', 0) for item in group]
      group_sum = sum(vals)
      group_avg = group_sum / window_size
      if group_sum > max_sum:
        max_sum = group_sum
      if group_avg > max_avg:
        max_avg = group_avg

    return max_sum, max_avg
  
  def calculate_risk_level(self, window):
    total_mm = sum(item.get('precipitation', 0) / 60 for item in window)

    if total_mm <= 0.2:
      risk_level = 1
    elif total_mm <= 0.5:
      risk_level = 2
    elif total_mm <= 1.5:
      risk_level = 3
    elif total_mm <= 3:
      risk_level = 4
    else:
      risk_level = 5
    return risk_level, total_mm

  def rain_risk_score(self, threshold=0.1, window_size=10):
    window = self.get_window(9, 31)
    persistent = self.has_persistent_rain(window, threshold, window_size)
    spike = self.has_spike(window, threshold)
    max_sum, max_avg = self.max_window_sum_avg(window, window_size)
    rain_detected = any(item.get('precipitation', 0) > threshold for item in window)
    risk_level, total_mm = self.calculate_risk_level(window)

    return {
      "rain_detected": rain_detected,
      "persistent_rain": persistent,
      "rain_spike": spike,
      "max_window_sum": max_sum,
      "max_window_avg": max_avg,
      "total_precip_mm": total_mm,
      "risk_level": risk_level
    }


# remove below 
if __name__ == "__main__":
  import json
  import os

  # Path to the test data file
  test_data_path = os.path.join(os.path.dirname(__file__), '../dataset/minutely-precipitation.json')
  with open(test_data_path, 'r') as f:
    test_data = json.load(f)

  print("Testing rain risk score on minutely datasets:\n")
  for name, dataset in test_data.items():
    minutely = dataset.get('minutely', [])
    scorer = RiskScore(minutely_data=minutely)
    result = scorer.rain_risk_score()
    print(f"{name}: {result}")
  