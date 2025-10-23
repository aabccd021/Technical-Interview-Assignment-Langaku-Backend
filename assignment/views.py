from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db import connection, IntegrityError
from drf_spectacular.utils import extend_schema

from .serializers import (
    RecordsJsonSerializer,
    UserSummaryQuerySerializer,
    UserSummaryResponseSerializer,
)


@extend_schema(
    request=RecordsJsonSerializer,
    responses={201: None, 409: None, 400: None},
)
@api_view(["POST"])
def recordsjson(request):
    """
    Record learning activity
    """
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
                VALUES (%(request_id)s, %(user_id)s, %(word_count)s, COALESCE(%(timestamp)s, CURRENT_TIMESTAMP))
                """,
                {
                    "request_id": request_id,
                    "user_id": user_id,
                    "word_count": word_count,
                    "timestamp": timestamp,
                },
            )
        return Response(None, status=status.HTTP_201_CREATED)
    except Exception as e:
        is_pk_conflicting = isinstance(e, IntegrityError) and str(e).startswith(
            'duplicate key value violates unique constraint "learning_log_pkey"'
        )
        if is_pk_conflicting:
            return Response(None, status=status.HTTP_409_CONFLICT)
        return Response(None, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    parameters=[UserSummaryQuerySerializer],
    responses={200: UserSummaryResponseSerializer(many=True)},
)
@api_view(["GET"])
def user_summary(request, user_id):
    """
    Simple moving average of words learned by a user for specific range and granularity
    """
    serializer = UserSummaryQuerySerializer(data=request.query_params)
    if not serializer.is_valid():
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    query_params = serializer.validated_data
    from_date = query_params.get("from")
    to_date = query_params.get("to")
    granularity = query_params.get("granularity")

    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT
                DATE_TRUNC(%(granularity)s, timestamp) AS period,
                AVG(word_count) AS average_words_learned
            FROM learning_log
            WHERE user_id = %(user_id)s 
              AND timestamp BETWEEN %(from_date)s AND %(to_date)s
            GROUP BY period
            ORDER BY period;
            """,
            {
                "user_id": user_id,
                "from_date": from_date,
                "to_date": to_date,
                "granularity": granularity,
            },
        )
        columns = [col[0] for col in cursor.description]
        rows = [dict(zip(columns, row)) for row in cursor.fetchall()]

    serialized_rows = UserSummaryResponseSerializer(rows, many=True).data
    return Response(serialized_rows, status=status.HTTP_200_OK)
