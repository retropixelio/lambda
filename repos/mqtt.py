import boto3

from conf import settings

class Mqtt:
    def __init__(self):
        self.client = boto3.client('iot-data', 
            region_name='us-east-1', 
            aws_access_key_id=settings.ACCESS_KEY_ID, 
            aws_secret_access_key=settings.ACCESS_SECRET_KEY
        )
        
    def publish(self,topic,payload):
        response = self.client.publish(
            topic=topic,
            qos=1,
            payload=payload
        )
        return response