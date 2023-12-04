# @@@SNIPSTART hello-weather-workflow-imports
from datetime import timedelta

from temporalio import workflow

with workflow.unsafe.imports_passed_through():
    from activities import WeatherActivities, WeatherParams
# @@@SNIPEND

# @@@SNIPSTART hello-weather-workflow-run
@workflow.defn
class WeatherWorkflow:
    @workflow.run
    async def run(self, weather_params: WeatherParams) -> list[dict]:
            return await workflow.execute_activity_method(
                WeatherActivities.get_weather,
                weather_params,
                schedule_to_close_timeout=timedelta(seconds=10),
            )
# @@@SNIPEND