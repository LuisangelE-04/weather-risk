'''
import time
from weather_location import WeatherLocation

def run_live_updates(lat, lon):
    while True:
        print(f"Fetching and processing data for {lat}, {lon} at {time.strftime('%Y-%m-%d %H:%M:%S')}")
        loc = WeatherLocation(lat, lon)
        # Assuming you have a method to process and print/store the rain score
        rain_score = loc.rain_score  # or call a method to get the latest score
        print(f"Rain score: {rain_score}")
        # TODO: Add code to update your database here
        print("Sleeping for 10 minutes...\n")
        time.sleep(600)  # Sleep for 10 minutes

if __name__ == "__main__":
    run_live_updates("29.8951", "-97.9093")
  
'''