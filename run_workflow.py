from flask import Flask, render_template
from temporalio.client import Client

from activities import WeatherParams
from workflows import WeatherWorkflow

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/weather")
async def get_weather():
    client = await Client.connect("localhost:7233")

    weather_params = WeatherParams("SEW", 123, 61)
    forecast_data = await client.execute_workflow(
        WeatherWorkflow.run,
        weather_params,
        id="weather-workflow-id",
        task_queue="my-task-queue",
    )

    simplified_forecast = []
    for period in forecast_data:
        period_data = {
            "name": period.get("name"),
            "startTime": period.get("startTime"),
            "endTime": period.get("endTime"),
            "temperature": period.get("temperature"),
            "temperatureUnit": period.get("temperatureUnit"),
            "windSpeed": period.get("windSpeed"),
            "windDirection": period.get("windDirection"),
            "shortForecast": period.get("shortForecast"),
            "detailedForecast": period.get("detailedForecast"),
        }
        simplified_forecast.append(period_data)

    return render_template("weather.html", forecast=simplified_forecast)


if __name__ == "__main__":
    app.run(debug=True)
