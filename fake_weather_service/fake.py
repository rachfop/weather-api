from aiohttp import web


async def mock_weather_service(request):
    return web.json_response(
        {
            "properties": {
                "periods": [
                    {"name": "Today", "temperature": 70, "shortForecast": "Sunny"},
                ]
            }
        }
    )


app = web.Application()
app.router.add_get(
    "/gridpoints/{office}/{gridX},{gridY}/forecast", mock_weather_service
)

# Run the app in your test setup
web.run_app(app, port=8080)
