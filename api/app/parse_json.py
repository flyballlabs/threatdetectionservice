import json

def json_type(data):
    try:
        return json.loads(data)
    except:
        raise ValueError('Malformed JSON')