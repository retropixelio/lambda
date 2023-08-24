from repos.firebase import FirebaseRepository
from repos.homegraph import HomeGraphRepository

from use_cases.iot import ConnectedUseCase

class ConnectedView:
    def get(self, request):
        firebase_repo = FirebaseRepository(None)
        homegraph_repo = HomeGraphRepository()
        use_case = ConnectedUseCase(firebase_repo, homegraph_repo)
        response = use_case.execute(request)
        return response