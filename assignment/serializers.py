from rest_framework import serializers
import datetime


class RecordsJsonSerializer(serializers.Serializer):
    request_id = serializers.UUIDField()
    user_id = serializers.CharField()
    word_count = serializers.IntegerField(min_value=0)
    timestamp = serializers.DateTimeField(required=False)


class UserSummaryQuerySerializer(serializers.Serializer):
    vars()["from"] = serializers.DateTimeField()  #
    to = serializers.DateTimeField()
    granularity = serializers.ChoiceField(choices=["hour", "day", "month"])


class UserSummaryResponseSerializer(serializers.Serializer):
    period = serializers.DateTimeField(default_timezone=datetime.timezone.utc)
    average_words_learned = serializers.FloatField()
