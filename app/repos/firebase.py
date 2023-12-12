import boto3
from boto3_type_annotations.dynamodb import ServiceResource

from domain.user import User, AccessKey
from domain.device import Device

dynamodb_client : ServiceResource = boto3.resource(
    'dynamodb',
    region_name='us-east-1',
)

class FirebaseRepository:
    def __init__(self, user):
        self.__user = user

    def get_user(self):
        return self.__user
    
    def get_user_info(self):
        users = dynamodb_client.Table('users')
        response = users.get_item(
            Key={'userId': self.get_user()}
        )
        item = response.get('Item')
        return User.from_dict(item) if item else User(user_id=self.get_user())
    
    def search_user(self, user_id: str):
        users = dynamodb_client.Table('users')
        response = users.get_item(
            Key={'userId': user_id}
        )
        item = response.get('Item')
        return User.from_dict(item) if item else None
        
    def create_user(self, user: User):
        users = dynamodb_client.Table('users')
        response = users.put_item(Item=user.to_dict())
        if response['ResponseMetadata']['HTTPStatusCode'] != 200:
            raise 'Error'
    
    def set_device(self, device: Device):
        users = dynamodb_client.Table('users')
        users.update_item(
            Key={'userId': self.get_user()},
            AttributeUpdates={
                'devices': device.to_dict(),
            },
        )
    
    def get_device(self, device_id):
        devices = dynamodb_client.Table('devices')
        response = devices.get_item(
            Key={'deviceId': device_id}
        )
        item = response.get('Item')
        return Device.from_dict(item) if item else None

    def set_state(self, device: Device):
        devices = dynamodb_client.Table('devices')
        response = devices.put_item(Item={key: value for key,value in device.to_dict().items() if value is not None})
        if response['ResponseMetadata']['HTTPStatusCode'] != 200:
            raise 'Error'

    def update_state(self, device, state, value):
        devices = dynamodb_client.Table('devices')
        devices.update_item(
            Key={'deviceId': device},
            AttributeUpdates={
                state: value,
            },
        )

    def get_credential(self, access_key):
        devices = dynamodb_client.Table('accessKeys')
        response = devices.get_item(
            Key={'thirdPartyCredential': access_key}
        )
        item = response.get('Item')
        return AccessKey.from_dict(item) if item else None
    
    def create_credential(self, access_key: AccessKey):
        access_keys = dynamodb_client.Table('accessKeys')
        response = access_keys.put_item(Item=access_key.to_dict())
        if response['ResponseMetadata']['HTTPStatusCode'] != 200:
            raise 'Error'
        
    def delete_credential(self, access_key: str):
        access_keys = dynamodb_client.Table('accessKeys')
        response = access_keys.delete_item(
            Key={'thirdPartyCredential': access_key}
        )
        if response['ResponseMetadata']['HTTPStatusCode'] != 200:
            raise 'Error'