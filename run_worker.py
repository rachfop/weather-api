import asyncio
import logging

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
        activities=[WeatherActivities().get_weather],
    )

    logging.info(f"Starting the worker....{client.identity}")

    try:
        await worker.run()
    finally:
        await WeatherActivities().close()


if __name__ == "__main__":
    asyncio.run(main())
