from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db import connection, IntegrityError


@api_view(["POST"])
def recordsjson(request):
    request_id = request.data["request_id"]
    user_id = request.data["user_id"]
    word_count = request.data["word_count"]

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO learning_log (request_id, user_id, word_count)
                VALUES (%s, %s, %s)
                """,
                [request_id, user_id, word_count],
            )
        return Response("OK", status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return Response(
            {"detail": "Duplicate request_id or integrity error."},
            status=status.HTTP_400_BAD_REQUEST,
        )
