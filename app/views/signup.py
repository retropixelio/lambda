from utils.api_view import APIView

from request_objects.signup import SignUp

from repos.firebase import FirebaseRepository

from use_cases.signup import SignUpUseCase

class SignupView(APIView):
    def post(self):
        request_object = SignUp.from_dict(self.request.json())
        firebase_repo = FirebaseRepository(self.user)
        use_case = SignUpUseCase(firebase_repo)
        response = use_case.execute(request_object)
        return response