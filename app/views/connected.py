from repos.firebase import FirebaseRepository
from repos.mqtt import Mqtt

from use_cases.iot import ConnectedUseCase

class ConnectedView:
    def get(self, request):
        firebase_repo = FirebaseRepository(None)
        mqtt_repo = Mqtt()
        use_case = ConnectedUseCase(firebase_repo, mqtt_repo)
        response = use_case.execute(request)
        return response