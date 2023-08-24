import boto3
from boto3_type_annotations.iot_data import Client

mqtt_client : Client = boto3.client('iot-data')

class Mqtt:        
    def publish(self,topic,payload):
        mqtt_client.publish(
            topic=topic,
            qos=1,
            payload=payload
        )