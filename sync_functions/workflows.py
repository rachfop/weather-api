# workflows.py
from datetime import timedelta
from temporalio import workflow

with workflow.unsafe.imports_passed_through():
    from activities import get_weather_activity, WeatherParams


@workflow.defn
class WeatherWorkflow:
    @workflow.run
    async def run(self, weather_params: WeatherParams) -> list[dict]:
        forecast_periods = await workflow.execute_activity(
            get_weather_activity,
            weather_params,
            schedule_to_close_timeout=timedelta(seconds=30),
        )

        return forecast_periods
