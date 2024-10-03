from typing import List

from typing_extensions import TypedDict

from vital_agent_kg_utils.vital_agent_rest_resource_client.tools.tool_results import ToolResults


class WeatherPrediction(TypedDict):
    """
    Represents a daily weather prediction.

    Attributes:
        date (str): The date of the prediction in ISO8601 format.
        weather_code (int): The weather condition code.
        temperature_max (float): The maximum temperature for the day.
        temperature_min (float): The minimum temperature for the day.
        apparent_temperature_max (float): The maximum apparent temperature for the day.
        apparent_temperature_min (float): The minimum apparent temperature for the day.
        sunrise (str): The time of sunrise in ISO8601 format.
        sunset (str): The time of sunset in ISO8601 format.
    """
    date: str
    weather_code: int
    temperature_max: float
    temperature_min: float
    apparent_temperature_max: float
    apparent_temperature_min: float
    sunrise: str
    sunset: str


class WeatherData(TypedDict):
    """
    Represents the weather data including current conditions and daily predictions.

    Attributes:
        latitude (float): The latitude of the location.
        longitude (float): The longitude of the location.
        timezone (str): The timezone of the location.
        current_temperature (float): The current temperature at the location.
        current_humidity (int): The current relative humidity at the location.
        wind_speed (float): The current wind speed at the location.
        daily_predictions (List[WeatherPrediction]): A list of daily weather predictions.
    """
    latitude: float
    longitude: float
    timezone: str
    current_temperature: float
    current_humidity: int
    wind_speed: float
    daily_predictions: List[WeatherPrediction]


class WeatherResponse(ToolResults):
    weather_data: WeatherData
