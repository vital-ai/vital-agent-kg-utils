import base64
import json
import logging
from typing import Dict
from com_vitalai_haleyai_question_domain.model.HaleyContainer import HaleyContainer
from vital_ai_vitalsigns.model.GraphObject import GraphObject
from vital_ai_vitalsigns.vitalsigns import VitalSigns


class VitalSignsUtils:
    @staticmethod
    def get_object_type(objects: list[GraphObject], type_value: str):
        for obj in objects:
            if obj.get_class_uri() == type_value:
                return obj
        return None

    @staticmethod
    def unpack_container(container: HaleyContainer):
        if container is None:
            return None
        container_string = str(container.serializedContainer)
        if container_string is None:
            return None

        decoded_bytes = base64.b64decode(container_string)

        json_string = decoded_bytes.decode('utf-8')

        # object_list = json.loads(json_string)

        vs = VitalSigns()

        object_list = vs.from_json_list(json_string)

        return object_list

    @staticmethod
    def pack_container(container: HaleyContainer, message_list: list[GraphObject]) -> HaleyContainer:
        if container is None:
            return None
        if message_list is None:
            return container
        if len(message_list) == 0:
            return container

        vs = VitalSigns()
        json_string = vs.to_json(message_list)
        encoded_bytes = json_string.encode('utf-8')
        container_string = base64.b64encode(encoded_bytes).decode('utf-8')
        container.serializedContainer = container_string
        return container

    @staticmethod
    def log_object_list(label: str, object_list: list[GraphObject]):
        logger = logging.getLogger()
        logger.info(f"-----------------\nLogging {label}:")
        for obj in object_list:
            logger.info(f"Object: {obj.to_json(pretty_print=False)}")
        logger.info("-----------------")
