from rest_framework import serializers


class AccountsSerializer(serializers.Serializer):
    account_id = serializers.CharField(read_only=True)
    account_owner = serializers.CharField(required=True)
    balance = serializers.FloatField(required=False)


class TransactionSerializer(serializers.Serializer):
    transaction_id = serializers.CharField(read_only=True)
    transaction_type = serializers.CharField(required=True)
    transaction_value = serializers.FloatField(required=True)
    transaction_date = serializers.CharField()
    transaction_description = serializers.CharField()


class ExtractSerializer(serializers.Serializer):
    extract_id = serializers.CharField(read_only=True)
    extract_date = serializers.CharField()
    former_account_balance = serializers.FloatField()
    current_account_balance = serializers.FloatField()
    transactions = TransactionSerializer(many=True, read_only=True)


class UpdateAccountBalanceSerializer(serializers.Serializer):
    balance = serializers.FloatField(required=True)
