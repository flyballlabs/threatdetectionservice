import json

def json_decode(data):
    try:
        return simplejson.loads(data)
        #return json.loads(data)
    except:
        raise ValueError('Malformed JSON')

def json_encode(data):
    try:
        return simplejson.dumps(value)
        #return json.dumps(data)
    except:
        raise ValueError('Malformed JSON')
    
def json_decode2(data):
    try:
        return json.JSONDecoder.decode(data)
    except:
        raise ValueError('Malformed JSON')

def json_encode2(data):
    try:
        return json.JSONEncoder.encode(data)
    except:
        raise ValueError('Malformed JSON')
    
    from flask import make_response

def custom_json_output(data, code, headers=None):
    dumped = json.dumps(data, cls=CustomEncoder)
    resp = make_response(dumped, code)
    resp.headers.extend(headers or {})
    return resp