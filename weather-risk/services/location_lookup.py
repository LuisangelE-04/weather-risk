from config_loader import Config
import psycopg2


cfg = Config()
DB_URL = cfg.database_url

def get_location_name(lat, lon):
  with psycopg2.connect(DB_URL) as conn:
    with conn.cursor() as cur:
      cur.execute(
        """
        SELECT name FROM location WHERE latitude = %s AND longitude = %s
        """,
        (lat, lon)
      )
      result = cur.fetchone()
      return result[0] if result else None