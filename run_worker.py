import asyncio

from temporalio.client import Client
from temporalio.worker import Worker

from activities import WeatherActivities
from workflows import WeatherWorkflow


async def main():
    client = await Client.connect("localhost:7233")
    worker = Worker(
        client,
        task_queue="my-task-queue",
        workflows=[WeatherWorkflow],
        activities=[WeatherActivities("https://api.weather.gov").get_weather],
    )
    try:
        await worker.run()
    finally:
        await WeatherActivities("https://api.weather.gov").close()


if __name__ == "__main__":
    asyncio.run(main())
