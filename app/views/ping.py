from utils.api_view import APIView

from repos.response import response_object

class PingView(APIView):
    def get(self):
        return response_object(None, 200)