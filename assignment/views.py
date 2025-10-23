from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db import connection, IntegrityError
from drf_spectacular.utils import extend_schema

from .serializers import RecordsJsonSerializer


@extend_schema(
    request=RecordsJsonSerializer,
    responses={201: None, 409: None, 400: None},
)
@api_view(["POST"])
def recordsjson(request):
    serializer = RecordsJsonSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    data = serializer.validated_data
    request_id = data.get("request_id")
    user_id = data.get("user_id")
    word_count = data.get("word_count")
    timestamp = data.get("timestamp", None)

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
        return Response(None, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response(None, status=status.HTTP_400_BAD_REQUEST)
