from rest_framework import serializers


class AccountsSerializer(serializers.Serializer):
    account_id = serializers.CharField(read_only=True)
    account_owner = serializers.CharField(required=True)
    balance = serializers.FloatField(required=False)


class ExtractSerializer(serializers.Serializer):
    extract_id = serializers.CharField(read_only=True)
    extract_date = serializers.DateTimeField()
    accounts = AccountsSerializer(read_only=True)
