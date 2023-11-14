import asyncio
import logging
from activities import WeatherActivities
from temporalio.client import Client
from temporalio.worker import Worker
from workflows import WeatherWorkflow

async def main():
    client = await Client.connect("localhost:7233")

    # Instantiate your activities
    activities = WeatherActivities()

    # Setup the worker
    worker = Worker(
        client,
        task_queue="my-task-queue",
        workflows=[WeatherWorkflow],
        activities=[activities.get_weather],
    )

    logging.info(f"Starting the worker....{client.identity}")

    try:
        await worker.run()
    finally:
        # Ensure the session is closed properly when the worker stops
        await activities.close()

if __name__ == "__main__":
    asyncio.run(main())
