from repos.firebase import FirebaseRepository

from use_cases.iot import ConnectedUseCase

class ConnectedView:
    def get(self, request):
        firebase_repo = FirebaseRepository(None)
        use_case = ConnectedUseCase(firebase_repo)
        response = use_case.execute(request)
        return response