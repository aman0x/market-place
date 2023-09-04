from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(["GET"])
def index(request):
    data = {'sample_data': 1234}
    return Response(data, status=200)
