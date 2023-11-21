import asyncio
import concurrent.futures

from temporalio.client import Client
from temporalio.worker import Worker

from activities import get_weather_activity
from workflows import WeatherWorkflow


async def main():
    client = await Client.connect("localhost:7233")

    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as activity_executor:
        worker = Worker(
            client,
            task_queue="my-task-queue",
            workflows=[WeatherWorkflow],
            activities=[get_weather_activity],
            activity_executor=activity_executor,
        )
        await worker.run()


if __name__ == "__main__":
    asyncio.run(main())
