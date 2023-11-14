from dataclasses import dataclass

from temporalio import activity
import requests


@dataclass
class WeatherParams:
    office: str
    gridX: int
    gridY: int


@activity.defn
async def get_weather_activity(input: WeatherParams) -> list[dict]:
    url = f"https://api.weather.gov/gridpoints/{input.office}/{input.gridX},{input.gridY}/forecast"
    response = requests.get(url)
    if response.status_code == 200:
        forecast_data = response.json()
        periods = forecast_data["properties"]["periods"]
        return periods
    else:
        raise Exception("Could not retrieve weather data")
