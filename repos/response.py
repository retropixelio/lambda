import json

def response_object(json_obj, status, headers = 'application/json'):
    return {
        'statusCode': status,
        'body': json.dumps(json_obj) if headers == 'application/json' else json_obj,
        'headers':{
            'Content-Type':headers
        }
    }

def redirect(url):
    return {
        'statusCode': 301,
        'headers': {
            'Location': url,
        }
    }