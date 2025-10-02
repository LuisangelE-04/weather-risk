import psycopg2
from psycopg2.extras import Json
from datetime import datetime, timezone
from ..config_loader import Config

cfg = Config()
DB_URL = cfg.database_url

def save_risk_score(location_id, risk_level, risk_details, raw_data, timestamp=None, conn=DB_URL):
  if timestamp is None:
    timestamp = datetime.now(timezone.utc)
  
  with psycopg2.connect(DB_URL) as conn:
    with conn.cursor() as cur:
      cur.execute("""
        INSERT INTO weatherevent (
            location_id,
            risk_level,
            risk_details,
            raw_data,
            timestamp
        ) VALUES (%s, %s, %s, %s, %s)
      """, (
        location_id,
        risk_level,
        Json(risk_details),
        Json(raw_data),
        timestamp
      ))
    conn.commit()

