from utils.api_view import APIView, TokenAuthentication

from repos.firebase import FirebaseRepository
from repos.mqtt import Mqtt

from use_cases.set import SetUseCase

from request_objects.set import Set

class SetView(APIView):
    authentication_classes = [TokenAuthentication]

    def post(self):
        request_obj = [Set.from_dict(item) for item in self.request.json()]
        firebase_repo = FirebaseRepository(self.user)
        mqtt_repo = Mqtt()
        use_case = SetUseCase(firebase_repo, mqtt_repo)
        response = use_case.execute(request_obj)
        return response