import boto3
from boto3_type_annotations.iot_data import Client

from conf import settings

mqtt_client : Client = boto3.client('iot-data', 
    region_name='us-east-1',
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
)

class Mqtt:        
    def publish(self,topic,payload):
        mqtt_client.publish(
            topic=topic,
            qos=1,
            payload=payload
        )