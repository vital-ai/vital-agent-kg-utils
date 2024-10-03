import json
import requests
from vital_agent_kg_utils.vital_agent_rest_resource_client.tools.weather.weather_request import WeatherRequest
from vital_agent_kg_utils.vital_agent_rest_resource_client.tools.weather.weather_response import WeatherData, \
    WeatherPrediction
from vital_agent_kg_utils.vital_agent_rest_resource_client.vital_agent_rest_resource_client import \
    VitalAgentRestResourceClient


def main():
    print("Weather Tool Test")

    client = VitalAgentRestResourceClient()

    weather_request = WeatherRequest(
        latitude=40.7128,
        longitude=-74.0060
    )

    tool_response = client.handle_tool_request("weather_tool", weather_request)

    weather_results = tool_response.tool_results

    print(json.dumps(weather_results, indent=4))


if __name__ == "__main__":
    main()

