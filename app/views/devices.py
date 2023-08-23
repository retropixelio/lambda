from utils.api_view import APIView, TokenAuthentication

from request_objects.device import Device

from repos.firebase import FirebaseRepository

from use_cases.devices import DevicesUseCase, AddDeviceUseCase

class DevicesView(APIView):
    authentication_classes = [TokenAuthentication]

    def get(self):
        firebase_repo = FirebaseRepository(self.user)
        use_case = DevicesUseCase(firebase_repo)
        response = use_case.execute()
        return response
    
    def post(self):
        request_object = Device.from_dict(self.request.json())
        firebase_repo = FirebaseRepository(self.user)
        use_case = AddDeviceUseCase(firebase_repo)
        response = use_case.execute(request_object)
        return response