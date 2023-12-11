from utils.api_view import APIView, FirebaseAuthentication

from repos.mqtt import Mqtt

from use_cases.set import SetUseCase

from request_objects.set import Set

class SetView(APIView):
    authentication_classes = [FirebaseAuthentication]

    def post(self):
        request_obj = [Set.from_dict(item) for item in self.request.json()]
        mqtt_repo = Mqtt()
        use_case = SetUseCase(mqtt_repo)
        response = use_case.execute(request_obj)
        return response