import json


class Utils:

    @staticmethod
    def json_to_object(json_object, class_type):
        any_data = json.loads(json_object)
        class_object = class_type(**any_data)
        return class_object
