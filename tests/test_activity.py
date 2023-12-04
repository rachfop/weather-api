# @@@SNIPSTART hello-weather-test-imports
import pytest
from aiohttp import web
from temporalio.testing import ActivityEnvironment

from activities import ForecastPeriod, WeatherActivities, WeatherParams
# @@@SNIPEND

# @@@SNIPSTART mocked-weather-service
# Mock weather service handler
async def mock_weather_service(request):
    return web.json_response(
        {
            "properties": {
                "periods": [
                    {
                        "name": "Today",
                        "startTime": "2023-12-04T09:00:00-05:00",
                        "endTime": "2023-12-04T21:00:00-05:00",
                        "temperature": 70,
                        "temperatureUnit": "F",
                        "windSpeed": "5 mph",
                        "windDirection": "NE",
                        "shortForecast": "Sunny",
                        "detailedForecast": "Clear skies with a high of 70°F. Northeast wind around 5 mph.",
                    },
                ]
            }
        }
    )
# @@@SNIPEND
# @@@SNIPSTART hello-weather-test-case
# Function-scoped fixture to start and stop the fake weather service
@pytest.fixture
async def start_fake_weather_service():
    app = web.Application()
    app.router.add_get(
        "/gridpoints/{office}/{grid_x},{grid_y}/forecast", mock_weather_service
    )

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "localhost", 8080)
    try:
        await site.start()
        yield
    finally:
        await runner.cleanup()
# @@@SNIPEND
# @@SNIPSTART hello-weather-test-fixtures
TEST_BASE_URL = "http://localhost:8080"


# Fixture for WeatherActivities
@pytest.fixture
async def weather_activities():
    activities = WeatherActivities(base_url=TEST_BASE_URL)
    yield activities
    await activities.close()


# Test case for WeatherActivities.get_weather
@pytest.mark.asyncio
@pytest.mark.usefixtures("start_fake_weather_service")
async def test_get_weather(weather_activities):
    input = WeatherParams(office="SEW", grid_x=123, grid_y=61)
    expected_output = [
        ForecastPeriod(
            name="Today",
            startTime="2023-12-04T09:00:00-05:00",
            endTime="2023-12-04T21:00:00-05:00",
            temperature=70,
            temperatureUnit="F",
            windSpeed="5 mph",
            windDirection="NE",
            shortForecast="Sunny",
            detailedForecast="Clear skies with a high of 70°F. Northeast wind around 5 mph.",
        ),
    ]

    activity_environment = ActivityEnvironment()
    result = await activity_environment.run(weather_activities.get_weather, input)
    assert result == expected_output
# @@@SNIPEND