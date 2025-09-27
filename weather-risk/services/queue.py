from .redis_client import redis_client

QUEUE_NAME = "risk_queue"

def push_to_queue(risk_payload):
  redis_client.xadd(QUEUE_NAME, {"data": risk_payload})

def read_from_queue(last_id="$", block=0):
  messages = redis_client.xread({QUEUE_NAME: last_id}, block=block)
  return messages