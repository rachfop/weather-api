import pytest
from aiohttp import web
from temporalio.testing import ActivityEnvironment

from activities import WeatherActivities, WeatherParams


# Mock weather service handler
async def mock_weather_service(request):
    return web.json_response(
        {
            "properties": {
                "periods": [
                    {"name": "Today", "temperature": 70, "shortForecast": "Sunny"},
                ]
            }
        }
    )

# Function-scoped fixture to start and stop the fake weather service
@pytest.fixture
async def start_fake_weather_service():
    app = web.Application()
    app.router.add_get("/gridpoints/{office}/{gridX},{gridY}/forecast", mock_weather_service)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, 'localhost', 8080)
    await site.start()

    yield

    await runner.cleanup()

# Fixture for WeatherActivities
@pytest.fixture
async def weather_activities():
    activities = WeatherActivities(base_url="http://localhost:8080")
    yield activities
    await activities.close()

# Test case for WeatherActivities.get_weather
@pytest.mark.asyncio
@pytest.mark.usefixtures("start_fake_weather_service")
@pytest.mark.parametrize(
    "input, expected_output",
    [
        (
            WeatherParams(office="SEW", gridX=123, gridY=61),
            [
                {"name": "Today", "temperature": 70, "shortForecast": "Sunny"},
            ],
        ),
    ],
)
async def test_get_weather(input, expected_output, weather_activities):
    activity_environment = ActivityEnvironment()
    result = await activity_environment.run(weather_activities.get_weather, input)
    assert result == expected_output
