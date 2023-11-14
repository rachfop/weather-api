import uuid

import pytest


from temporalio.worker import Worker
from temporalio.testing import ActivityEnvironment
from activities import get_weather_activity, WeatherParams
from temporalio.client import Client
from temporalio import activity
from temporalio.worker import Worker
from workflows import WeatherWorkflow


mocked_forecast_data = [
    {
        "number": 1,
        "name": "Today",
        "startTime": "2023-11-08T09:00:00-05:00",
        "endTime": "2023-11-08T15:00:00-05:00",
        "isDaytime": True,
        "temperature": 70,
        "temperatureUnit": "F",
        "windSpeed": "5 to 10 mph",
        "windDirection": "S",
        "shortForecast": "Sunny",
        "detailedForecast": "Sunny, with a high near 70.",
    },
]


@pytest.fixture
def mocked_session(mocker):
    async def json():
        return {"properties": {"periods": mocked_forecast_data}}

    response_mock = mocker.Mock(status=200, json=json)
    session_mock = mocker.Mock(get=mocker.AsyncMock(return_value=response_mock))

    return session_mock


@pytest.mark.asyncio
async def test_get_weather_activity(mocked_session):
    activity_environment = ActivityEnvironment()
    test_params = WeatherParams(office="YourOffice", gridX=123, gridY=456)

    # Replace get_weather_activity's aiohttp.ClientSession with the mocked session
    with activity_environment.mock(aiohttp.ClientSession, mocked_session):
        # Run the activity with mocked session and check if the result matches the mocked forecast data
        result = await activity_environment.run(get_weather_activity, test_params)
        assert result == mocked_forecast_data
