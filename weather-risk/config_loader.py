import os
import yaml

try:
  from dotenv import load_dotenv
  load_dotenv()
except ImportError:
  print("ptyon-dotenv not installed, using system environment variables")

class Config:
  def __init__(self, path=None):
    if path is None:
      path = os.path.join(os.path.dirname(__file__), "config.yaml")

    data = {}
    if os.path.exists(path):
      with open(path, "r") as f:
        data = yaml.safe_load(f) or {}
    
    self.database_url = os.getenv("DATABASE_URL", data.get("database_url"))
    self.data_sources = data.get("data_sources", [])
    self.log_path = data.get("log_path")
    retry_config = data.get("retry", {})
    self.retry_max = retry_config.get("max", 3)
    self.retry_backoff = retry_config.get("backoff", 2)
