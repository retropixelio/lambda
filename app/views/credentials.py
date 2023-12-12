from utils.api_view import APIView, FirebaseAuthentication

from repos.firebase import FirebaseRepository

from use_cases.credentials import CredentialsUseCase

class CredentialsView(APIView):
    authentication_classes = [FirebaseAuthentication]

    def get(self):
        firebase_repo = FirebaseRepository(self.user)
        use_case = CredentialsUseCase(firebase_repo)
        response = use_case.execute()
        return response