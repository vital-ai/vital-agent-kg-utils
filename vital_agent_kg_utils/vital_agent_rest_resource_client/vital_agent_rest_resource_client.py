from typing import List, Type, Tuple

import requests
from ai_haley_kg_domain.model.KGInteraction import KGInteraction
from kgraphservice.kgraph_service_inf import KGraphServiceInterface, KGFP, KGN, G
from kgraphservice.ontology.ontology_query_manager import OntologyQueryManager
from typing_extensions import TypedDict
from vital_ai_vitalsigns.query.part_list import PartList
from vital_ai_vitalsigns.query.result_list import ResultList
from vital_ai_vitalsigns.service.vital_namespace import VitalNamespace
from vital_ai_vitalsigns.service.vital_service_status import VitalServiceStatus

from vital_agent_kg_utils.vital_agent_rest_resource_client.tool_service_interface import ToolServiceInterface
from vital_agent_kg_utils.vital_agent_rest_resource_client.tools.tool_parameters import ToolParameters
from vital_agent_kg_utils.vital_agent_rest_resource_client.tools.tool_request import ToolRequest
from vital_agent_kg_utils.vital_agent_rest_resource_client.tools.tool_response import ToolResponse
from vital_agent_kg_utils.vital_agent_rest_resource_client.tools.tool_results import ToolResults
from vital_agent_kg_utils.vital_agent_rest_resource_client.tools.weather.weather_response import WeatherResponse, \
    WeatherPrediction, WeatherData


# client to the python webservice which provides access to tools
# and queries to kgraph service (graph and vector db)

def parse_weather_response(response_json: dict) -> WeatherData:
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


class VitalAgentRestResourceClient(KGraphServiceInterface, ToolServiceInterface):

    # Tools

    def handle_tool_request(self, tool_name: str, tool_parameters: ToolParameters) -> ToolResults:

        tool_request = ToolRequest(
            tool=tool_name,
            tool_parameters=tool_parameters
        )

        url = "http://localhost:8008/tool"

        # url = "http://internal-vital-agent-resource-rest-lb-1305845817.us-east-1.elb.amazonaws.com:8008/tool"

        # url = "http://vital-agent-resource-rest-lb.apichatai.com:8008/tool"

        tool_request_dict = tool_request.to_dict()

        response = requests.post(url, json=tool_request_dict)

        print(f"Status Code: {response.status_code}")
        print("Response JSON:")

        response_json = response.json()

        weather_data = parse_weather_response(response_json)

        weather_response = WeatherResponse(
            weather_data=weather_data
        )

        return weather_response

    # KGService calls

    def get_ontology_query_manager(self) -> OntologyQueryManager:
        pass

    def get_graph(self, graph_uri: str) -> VitalNamespace:
        pass

    def list_graphs(self) -> List[VitalNamespace]:
        pass

    def check_create_graph(self, graph_uri: str) -> bool:
        pass

    def create_graph(self, graph_uri: str) -> bool:
        pass

    def delete_graph(self, graph_uri: str) -> bool:
        pass

    def purge_graph(self, graph_uri: str) -> bool:
        pass

    def get_graph_all_objects(self, graph_uri: str, limit=100, offset=0) -> ResultList:
        pass

    def insert_object(self, graph_uri: str, graph_object: G) -> VitalServiceStatus:
        pass

    def insert_object_list(self, graph_uri: str, graph_object_list: List[G]) -> VitalServiceStatus:
        pass

    def update_object(self, graph_object: G, graph_uri: str, *, upsert: bool = False) -> VitalServiceStatus:
        pass

    def update_object_list(self, graph_object_list: List[G], graph_uri: str, *,
                           upsert: bool = False) -> VitalServiceStatus:
        pass

    def get_object(self, object_uri: str, graph_uri: str | None = None) -> G:
        pass

    def get_object_list(self, object_uri_list: List[str], graph_uri: str | None = None) -> ResultList:
        pass

    def delete_object(self, object_uri: str, graph_uri: str | None = None) -> VitalServiceStatus:
        pass

    def delete_object_list(self, object_uri_list: List[str], graph_uri: str | None = None) -> VitalServiceStatus:
        pass

    def filter_query(self, graph_uri: str, sparql_query: str) -> ResultList:
        pass

    def query(self, graph_uri: str, sparql_query: str) -> ResultList:
        pass

    def query_construct(self, graph_uri: str, sparql_query: str, binding_list: List[Tuple[str, str]]) -> ResultList:
        pass

    def get_interaction_list(self, graph_uri: str, limit=100, offset=0) -> ResultList:
        pass

    def get_interaction_graph(self, graph_uri: str, interaction: KGInteraction, limit=100, offset=0) -> ResultList:
        pass

    def get_interaction_frames(self, graph_uri: str, interaction: KGInteraction, limit=100, offset=0) -> PartList:
        pass

    def get_interaction_nodes(self, graph_uri: str, interaction: KGInteraction, kgnode_type: Type[KGN], limit=100,
                              offset=0) -> ResultList:
        pass

    def get_frame(self, graph_uri: str, frame_uri: str, limit=100, offset=0) -> KGFP:
        pass

    def get_frames(self, graph_uri: str, frame_uri_list: List[str], limit=100, offset=0) -> PartList:
        pass

    def get_frame_id(self, graph_uri: str, frame_id: str, limit=100, offset=0) -> KGFP:
        pass

    def get_frames_id(self, graph_uri: str, frame_id_list: List[str], limit=100, offset=0) -> PartList:
        pass

    def get_frames_root(self, graph_uri: str, root_uri: str, limit=100, offset=0) -> PartList:
        pass

    def get_graph_objects_type(self, graph_uri: str, class_uri: str, include_subclasses=True, limit=100,
                               offset=0) -> ResultList:
        pass

    def get_graph_objects_tag(self, graph_uri: str, kg_graph_uri: str, limit=100, offset=0) -> ResultList:
        pass

    def delete_frame(self, graph_uri: str, frame_uri: str) -> VitalServiceStatus:
        pass

    def delete_frames(self, graph_uri: str, frame_uri_list: List[str]) -> VitalServiceStatus:
        pass

    def delete_frame_id(self, graph_uri: str, frame_id: str) -> VitalServiceStatus:
        pass

    def delete_frames_id(self, graph_uri: str, frame_id_list: List[str]) -> VitalServiceStatus:
        pass

    def delete_graph_objects_tag(self, graph_uri: str, kg_graph_uri: str) -> VitalServiceStatus:
        pass
