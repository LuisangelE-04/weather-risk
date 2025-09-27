import time
from .queue import read_from_queue

def process_risk_event(risk_payload):
  print("Recieved risk event:", risk_payload)

def main():
  last_id = "$"
  print("Listening for risk events...")
  while True:
    messages = read_from_queue(last_id=last_id, block=0)
    if messages:
      for stream, msgs in messages:
        for msg_id, msg_data in msgs:
          risk_payload = msg_data["data"]
          process_risk_event(risk_payload)
          last_id = msg_id
    else:
      print("No new messages, waiting...")

if __name__ == "__main__":
  main()
