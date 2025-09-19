import os
import yaml

class Config:
  def __init__(self, path=None):
    if path is None:
      path = os.path.join(os.path.dirname(__file__), "config.yaml")
    if os.path.exists(path):
      with open(path, "r") as f:
        data = yaml.safe_load(f)
    
    self.database_url = data["database_url"]
    self.user_agent = data["user_agent"]
    self.data_source = data["data_source"]
    self.log_path = data["log_path"]
    self.retry_max = data["retry"]["max"]
    self.retry_backoff = data["retry"]["backoff"]

print("Done building Config File")