from vital_agent_kg_utils.vital_agent_rest_resource_client.tools.tool_parameters import ToolParameters


class WeatherRequest(ToolParameters):
    latitude: float
    longitude: float
