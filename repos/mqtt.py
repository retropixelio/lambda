import boto3

class Mqtt:
    def __init__(self):
        self.client = boto3.client('iot-data', 
            region_name='us-east-1'
        )
        
    def publish(self,topic,payload):
        self.client.publish(
            topic=topic,
            qos=1,
            payload=payload
        )