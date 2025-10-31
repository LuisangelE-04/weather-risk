from .redis_client import redis_client
import json
import time

def cache_latest_risk(lat, lon, risk_payload, timestamp=None):
  key = f"risk:{lat},{lon}"
  if timestamp is None:
    timestamp = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
  value = json.dumps({
    "risk": risk_payload,
    "timestamp": timestamp
  })
  redis_client.set(key, value)

def get_latest_risk(lat, lon):
  key = f"risk:{lat},{lon}"
  return redis_client.get(key)