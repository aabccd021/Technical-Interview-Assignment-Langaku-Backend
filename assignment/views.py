from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(["POST"])
def recordsjson(request):
    word_count = request.data["word_count"]
    return Response("OK", status=status.HTTP_200_OK)
