from utils.api_view import APIView

from request_objects.refresh import Refresh

from use_cases.refresh import RefreshUseCase

class RefreshView(APIView):
    def post(self):
        request_object = Refresh.from_dict(self.request.json())
        use_case = RefreshUseCase()
        response = use_case.execute(request_object)
        return response