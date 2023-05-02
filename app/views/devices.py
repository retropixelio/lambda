from utils.api_view import APIView, TokenAuthentication

from repos.firebase import FirebaseRepository

from use_cases.devices import DevicesUseCase

class DevicesView(APIView):
    authentication_classes = [TokenAuthentication]

    def get(self):
        firebase_repo = FirebaseRepository(self.user)
        use_case = DevicesUseCase(firebase_repo)
        response = use_case.execute()
        return response