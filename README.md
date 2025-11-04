# Weather Risk

The following application uses real time weather data based off the openweathermap API and NWS API to determine weather risk across various locations.

# How to run current application

## Starting Redis Server
Used brew to install redis, [documentation](<https://redis.io/docs/latest/operate/oss_and_stack/install/archive/install-redis/install-redis-on-mac-os/>) here.

To start in background run:
```zsh
brew services start redis
```
To stop the redis service run:
```zsh
brew services stop redis
```

## Starting Weather Monitor

```zsh
python -m weahter_risk.live_updater
```

## Starting Consumer Script

Based on the application and number of consumers but for one single consumer in this current build you do. the following:

```zsh
python -m weahter_risk.services.consumer
```