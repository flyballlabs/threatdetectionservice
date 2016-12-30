import json

def json_decode(data):
    try:
        return json.loads(data)
    except:
        raise ValueError('Malformed JSON')

def json_encode(data):
    try:
        return json.dumps(data)
    except:
        raise ValueError('Malformed JSON')
