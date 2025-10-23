from rest_framework import serializers


class RecordsJsonSerializer(serializers.Serializer):
    request_id = serializers.UUIDField()
    user_id = serializers.CharField()
    word_count = serializers.IntegerField(min_value=0)
    timestamp = serializers.DateTimeField(required=False)
