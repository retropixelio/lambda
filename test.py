import boto3
import json

ACCESS_KEY_ID = 'AKIATTIA7Z53SQYXT5VA'
ACCESS_SECRET_KEY = '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'

client = boto3.client('lambda', 
    region_name='us-east-1', 
    aws_access_key_id=ACCESS_KEY_ID, 
    aws_secret_access_key=ACCESS_SECRET_KEY
)

payload = json.dumps({"hola":"q ace"})
print(payload)

response = client.invoke(FunctionName = 'api', Payload = payload)
payload = json.loads(response['Payload'].read())
body = json.loads(payload['body'])
print(body)

# id = 'LIGHT_aznnl6JAJUxIyPFKgGDEA'

# mqtt = boto3.client('iot-data', 
#     region_name='us-east-1', 
#     aws_access_key_id=ACCESS_KEY_ID, 
#     aws_secret_access_key=ACCESS_SECRET_KEY
# )

# mqtt.publish(
#     topic=f"{id}/OnOff",
#     qos=1,
#     payload="false"
# )