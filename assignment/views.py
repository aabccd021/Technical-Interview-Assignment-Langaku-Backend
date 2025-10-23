from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db import connection, IntegrityError


@api_view(["POST"])
def recordsjson(request):
    try:
        request_id = request.data["request_id"]
        user_id = request.data["user_id"]
        word_count = request.data["word_count"]
        timestamp = request.data.get("timestamp", None)
    except KeyError as e:
        return Response(None, status=status.HTTP_400_BAD_REQUEST)

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO learning_log (request_id, user_id, word_count, timestamp)
                VALUES (%s, %s, %s, COALESCE(%s, CURRENT_TIMESTAMP))
                """,
                [request_id, user_id, word_count, timestamp],
            )
        return Response(None, status=status.HTTP_201_CREATED)
    except IntegrityError as e:
        print(e)
        return Response(None, status=status.HTTP_409_CONFLICT)
    except Exception as e:
        print(e)
        return Response(None, status=status.HTTP_400_BAD_REQUEST)
