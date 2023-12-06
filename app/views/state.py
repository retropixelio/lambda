from repos.firebase import FirebaseRepository
from repos.homegraph import HomeGraphRepository

from use_cases.iot import StateUseCase

class StateView:
    def get(self, request):
        firebase_repo = FirebaseRepository(None)
        homegraph_repo = HomeGraphRepository()
        use_case = StateUseCase(firebase_repo, homegraph_repo)
        response = use_case.execute(request)
        return response