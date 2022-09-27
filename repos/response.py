import json

def response_object(json_obj, status, headers = 'application/json'):
    return {
        'statusCode': status,
        'body': json.dumps(json_obj),
        'headers':{
            'Content-Type':headers
        }
    }