# @@@SNIPSTART hello-weather-activities-imports
import urllib.parse
from dataclasses import dataclass

import aiohttp
from temporalio import activity
from temporalio.exceptions import ApplicationError
# @@@SNIPEND
# @@@SNIPSTART hello-weather-activity-dataclass
@dataclass
class ForecastPeriod:
    name: str
    startTime: str
    endTime: str
    temperature: int
    temperatureUnit: str
    windSpeed: str
    windDirection: str
    shortForecast: str
    detailedForecast: str


@dataclass
class WeatherParams:
    office: str
    grid_x: int
    grid_y: int
# @@@SNIPEND
# @@@SNIPSTART hello-weather-activity-class
class WeatherActivities:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.session = aiohttp.ClientSession()

    @activity.defn
    async def get_weather(self, input: WeatherParams) -> list[ForecastPeriod]:
        encoded_office = urllib.parse.quote_plus(input.office)
        url = f"{self.base_url}/gridpoints/{encoded_office}/{input.grid_x},{input.grid_y}/forecast"

        async with self.session.get(url) as response:
            # Non-retryable client errors (400-499)
            if 400 <= response.status < 500:
                response_text = await response.text()
                raise ApplicationError(
                    f"Client error, status code {response.status}, response: {response_text}",
                    non_retryable=True,
                )

            elif response.status == 200:
                forecast_data = await response.json()
                periods = [
                    ForecastPeriod(
                        name=period["name"],
                        startTime=period["startTime"],
                        endTime=period["endTime"],
                        temperature=period["temperature"],
                        temperatureUnit=period["temperatureUnit"],
                        windSpeed=period["windSpeed"],
                        windDirection=period["windDirection"],
                        shortForecast=period["shortForecast"],
                        detailedForecast=period["detailedForecast"],
                    )
                    for period in forecast_data["properties"]["periods"]
                ]
                return periods
            else:
                # For other errors, you can customize the behavior as needed
                response_text = await response.text()
                raise ApplicationError(
                    f"Server error or unexpected status, status code {response.status}, response: {response_text}"
                )

    async def close(self):
        await self.session.close()
# @@@SNIPEND