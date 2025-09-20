class RiskScore:
  def __init__(self, minutely_data=None, hourly_data=None, daily_data=None):
    self.minutely_data = minutely_data or []
    self.hourly_data = hourly_data or []
    self.daily_data = daily_data or []

  def rain_risk_score(self):
    '''
    implement a rain risk score assesement
    '''
    pass