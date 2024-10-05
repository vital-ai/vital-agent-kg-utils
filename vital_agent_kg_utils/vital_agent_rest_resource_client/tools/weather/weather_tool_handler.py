import uuid

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

        # assign a unique id to this data response
        guid = uuid.uuid4()

        weather_data = WeatherData(
            tool_request_guid=str(guid),
            tool_data_class="WeatherData",
            latitude=data['latitude'],
            longitude=data['longitude'],
            timezone=data['timezone'],
            current_temperature=data['current']['temperature_2m'],
            current_humidity=data['current']['relative_humidity_2m'],
            wind_speed=data['current']['wind_speed_10m'],
            daily_predictions=daily_predictions
        )

        return weather_data

    @staticmethod
    def get_weather_code_id(weather_code: int) -> str:
        """
        Returns the icon name corresponding to the weather code.

        Args:
            weather_code (int): The weather condition code.

        Returns:
            str: The icon name.
        """
        weather_code_mapping = {
            0: "wi-day-sunny",  # Clear sky
            1: "wi-day-sunny-overcast",  # Mainly clear
            2: "wi-day-cloudy",  # Partly cloudy
            3: "wi-day-cloudy",  # Overcast
            45: "wi-fog",  # Fog
            48: "wi-fog",  # Depositing rime fog
            51: "wi-day-showers",  # Drizzle: Light
            53: "wi-day-showers",  # Drizzle: Moderate
            55: "wi-day-storm-showers",  # Drizzle: Dense
            61: "wi-day-rain",  # Rain: Slight
            63: "wi-day-rain",  # Rain: Moderate
            65: "wi-day-rain",  # Rain: Heavy
            66: "wi-day-sleet",  # Freezing rain: Light
            67: "wi-day-sleet",  # Freezing rain: Heavy
            71: "wi-day-snow",  # Snow fall: Slight
            73: "wi-day-snow",  # Snow fall: Moderate
            75: "wi-day-snow",  # Snow fall: Heavy
            77: "wi-snowflake-cold",  # Snow grains
            80: "wi-day-showers",  # Rain showers: Slight
            81: "wi-day-showers",  # Rain showers: Moderate
            82: "wi-day-showers",  # Rain showers: Violent
            85: "wi-day-snow",  # Snow showers: Slight
            86: "wi-day-snow",  # Snow showers: Heavy
            95: "wi-thunderstorm",  # Thunderstorm: Slight or moderate
            96: "wi-thunderstorm",  # Thunderstorm with slight hail
            99: "wi-thunderstorm",  # Thunderstorm with heavy hail

        }
        return weather_code_mapping.get(weather_code, "wi-na")