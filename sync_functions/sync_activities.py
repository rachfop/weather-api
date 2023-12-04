from dataclasses import dataclass

import requests
from temporalio import activity


@dataclass
class WeatherParams:
    office: str
    grid_x: int
    grid_y: int


@activity.defn
async def get_weather_activity(input: WeatherParams) -> list[dict]:
    url = f"https://api.weather.gov/gridpoints/{input.office}/{input.grid_x},{input.grid_y}/forecast"
    response = requests.get(url)
    if response.status_code == 200:
        forecast_data = response.json()
        periods = forecast_data["properties"]["periods"]
        return periods
    else:
        raise Exception("Could not retrieve weather data")
