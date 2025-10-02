# Weather Risk

The following application uses real time weather data based off the openweathermap API and NWS API to determine weather risk across various locations.

# How to run current application

## Starting Redis Server

```zsh
redis-cli
```

## Starting Weather Monitor

```zsh
python -m live_updater
```

## Starting Consumer Script

Based on the application and number of consumers but for one single consumer in this current build you do. the following:

```zsh
python -m services.consumer
```