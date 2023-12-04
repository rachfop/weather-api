# @@@SNIPSTART hello-weather-client-imports
from flask import Flask, render_template
from temporalio.client import Client

from activities import WeatherParams
from workflows import WeatherWorkflow
# @@@SNIPEND
# @@@SNIPSTART hello-weather-client-init
app = Flask(__name__)


async def get_client() -> Client:
    return await Client.connect("localhost:7233")


@app.route("/")
def home():
    return render_template("index.html")
# @@@SNIPEND
# @@@SNIPSTART hello-weather-client
@app.route("/weather")
async def get_weather():
    client = await get_client()
    weather_params = WeatherParams("SEW", 123, 61)
    forecast_data = await client.execute_workflow(
        WeatherWorkflow.run,
        weather_params,
        id="weather-workflow-id",
        task_queue="weather-task-queue",
    )
    return render_template("weather.html", forecast=forecast_data)


if __name__ == "__main__":
    app.run(debug=True)
# @@@SNIPEND