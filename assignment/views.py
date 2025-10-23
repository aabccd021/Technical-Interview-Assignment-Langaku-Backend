from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db import connection, IntegrityError


@api_view(["POST"])
def recordsjson(request):
    request_id = request.data.get("request_id", None)
    user_id = request.data.get("user_id", None)
    word_count = request.data.get("word_count", None)
    timestamp = request.data.get("timestamp", None)

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
        if str(e).startswith(
            'duplicate key value violates unique constraint "learning_log_pkey"'
        ):
            return Response(None, status=status.HTTP_409_CONFLICT)
        print(e)
        return Response(None, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print(e)
        return Response(None, status=status.HTTP_400_BAD_REQUEST)
