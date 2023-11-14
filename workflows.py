# workflows.py
from datetime import timedelta
from temporalio import workflow

with workflow.unsafe.imports_passed_through():
    from activities import WeatherActivities, WeatherParams


@workflow.defn
class WeatherWorkflow:
    @workflow.run
    async def run(self, weather_params: WeatherParams) -> list[dict]:
        forecast_periods = await workflow.execute_activity(
            WeatherActivities.get_weather,
            weather_params,
            schedule_to_close_timeout=timedelta(seconds=10),
        )

        return forecast_periods
