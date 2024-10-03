from vital_agent_kg_utils.vital_agent_rest_resource_client.tools.tool_handler import ToolHandler
from vital_agent_kg_utils.vital_agent_rest_resource_client.tools.tool_results import ToolResults
from vital_agent_kg_utils.vital_agent_rest_resource_client.tools.weather.weather_response import WeatherData, \
    WeatherPrediction, WeatherResponse


class WeatherToolHandler(ToolHandler):

    def handle_response(self, response_json: dict) -> ToolResults:

        weather_data = self.parse_weather_response(response_json)

        weather_response = WeatherResponse(
            weather_data=weather_data
        )

        return weather_response

    def parse_weather_response(self, response_json: dict) -> WeatherData:
        data = response_json
        daily = data['daily']

        daily_predictions = [
            WeatherPrediction(
                date=daily['time'][i],
                weather_code=daily['weather_code'][i],
                temperature_max=daily['temperature_2m_max'][i],
                temperature_min=daily['temperature_2m_min'][i],
                apparent_temperature_max=daily['apparent_temperature_max'][i],
                apparent_temperature_min=daily['apparent_temperature_min'][i],
                sunrise=daily['sunrise'][i],
                sunset=daily['sunset'][i]
            )
            for i in range(len(daily['time']))
        ]

        weather_data = WeatherData(
            latitude=data['latitude'],
            longitude=data['longitude'],
            timezone=data['timezone'],
            current_temperature=data['current']['temperature_2m'],
            current_humidity=data['current']['relative_humidity_2m'],
            wind_speed=data['current']['wind_speed_10m'],
            daily_predictions=daily_predictions
        )

        return weather_data