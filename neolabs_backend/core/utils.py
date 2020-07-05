import json


def is_json_serializable(value):
    try:
        json.dumps(value)
        return True
    except TypeError:
        return False
