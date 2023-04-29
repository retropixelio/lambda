from utils.api_view import APIView, TokenAuthentication

from repos.firebase import FirebaseRepository
from repos.mqtt import Mqtt

from use_cases.google import SmarthomeUseCase

from request_objects.set import Set

class SmarthomeView(APIView):
    authentication_classes = [TokenAuthentication]

    def post(self):
        request_obj = self.request.json()
        firebase_repo = FirebaseRepository(self.user)
        mqtt_repo = Mqtt()
        use_case = SmarthomeUseCase(firebase_repo, mqtt_repo)
        response = use_case.execute(request_obj)
        return response