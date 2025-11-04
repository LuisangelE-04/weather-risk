from statsmodels.tsa.arima.model import ARIMA
_HAS_ARIMA = True

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
    series = [max(0.0, (item.get('precipitation', 0) or 0)) for item in window]
    baseline_total_mm = sum(v / 60.0 for v in series)
    effective_total_mm = baseline_total_mm

    rain_detected = any(v > 0 for v in series)
    if rain_detected and _HAS_ARIMA and len(series) >= 8:
      try:
        model = ARIMA(series, order=(1, 0, 0), enforce_stationarity=False, enforce_invertibility=False)
        fit = model.fit(method_kwargs={"warn_convergence": False})
        steps = 30
        forecast = fit.forecast(steps=steps)
        forecast_total_mm = sum(max(0.0, float(v)) / 60.0 for v in forecast)
        effective_total_mm = max(baseline_total_mm, forecast_total_mm)
      except Exception:
        effective_total_mm = baseline_total_mm


    if effective_total_mm <= 0.2:
      risk_level = 1
    elif effective_total_mm <= 0.5:
      risk_level = 2
    elif effective_total_mm <= 1.5:
      risk_level = 3
    elif effective_total_mm <= 3:
      risk_level = 4
    else:
      risk_level = 5
    return risk_level, effective_total_mm

  def rain_risk_score(self, threshold=0.1, window_size=10):
    window = self.get_window(9, 40)
    persistent = self.has_persistent_rain(window, threshold, window_size)
    spike = self.has_spike(window, threshold)
    max_sum, max_avg = self.max_window_sum_avg(window, window_size)
    rain_detected = any(item.get('precipitation', 0) > threshold for item in window)
    risk_level, total_mm = self.calculate_risk_level(window)

    paylaod = {
      "rain_detected": rain_detected,
      "persistent_rain": persistent,
      "rain_spike": spike,
      "max_window_sum": max_sum,
      "max_window_avg": max_avg,
      "total_precip_mm": total_mm,
      "risk_level": risk_level
    }

    return paylaod
