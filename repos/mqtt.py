import boto3

class Mqtt:
    def __init__(self):
        self.client = boto3.client('iot-data', 
            region_name='us-east-1',
            aws_access_key_id='AKIATTIA7Z53XKUEPR6Q', 
            aws_secret_access_key='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'
        )
        
    def publish(self,topic,payload):
        response = self.client.publish(
            topic=topic,
            qos=1,
            payload=payload
        )
        return response