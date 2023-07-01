from repos.firebase import FirebaseRepository

from use_cases.iot import StateUseCase

class StateView:
    def get(self, state):
        firebase_repo = FirebaseRepository(None)
        use_case = StateUseCase(firebase_repo)
        response = use_case.execute(state)
        return response