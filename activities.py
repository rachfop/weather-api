from dataclasses import dataclass
import aiohttp
from aiohttp import TCPConnector
from temporalio import activity
import socket

@dataclass
class WeatherParams:
    office: str
    gridX: int
    gridY: int

class WeatherActivities:
    def __init__(self):
        # This will force the use of IPv4 and not IPv6 and bypass SSL certificate verification
        connector = TCPConnector(family=socket.AF_INET, ssl=False)
        self.session = aiohttp.ClientSession(connector=connector)

    @activity.defn
    async def get_weather(self, input: WeatherParams) -> list[dict]:
        url = f"https://api.weather.gov/gridpoints/{input.office}/{input.gridX},{input.gridY}/forecast"

        async with self.session.get(url) as response:
            if response.status == 200:
                forecast_data = await response.json()
                periods = forecast_data["properties"]["periods"]
                return periods
            else:
                response_text = await response.text()
                raise Exception(
                    f"Could not retrieve weather data, status code {response.status}, response: {response_text}"
                )

    async def close(self):
        await self.session.close()
