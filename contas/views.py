from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import APIView, api_view
from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_401_UNAUTHORIZED,
    HTTP_403_FORBIDDEN,
    HTTP_422_UNPROCESSABLE_ENTITY,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK,
)

from contas.models import Extract, Transactions, Accounts
from contas.serializers import (
    AccountsSerializer,
    ExtractSerializer,
    UpdateAccountBalanceSerializer,
)


class AccountsView(APIView):
    def post(self, request: Request):
        serializer = AccountsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        found_account = Accounts.objects.filter(
            account_owner=serializer.validated_data["account_owner"]
        )

        if found_account:
            return Response(
                {"message": "Requested account owner already exists"},
                HTTP_422_UNPROCESSABLE_ENTITY,
            )
        account = Accounts.objects.create(**serializer.validated_data)
        serializer = AccountsSerializer(account)

        return Response(serializer.data, HTTP_201_CREATED)

    def get(self, request: Request):
        found_accounts = Accounts.objects.all()
        serializer = [AccountsSerializer(account).data for account in found_accounts]
        return Response(serializer)

    def patch(self, request: Request, action: None, account_id):
        serializer = UpdateAccountBalanceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        found_account = Accounts.objects.get(account_id=account_id)

        if not found_account:
            return Response(
                {"message": "Account for the requested account_id does not exist"},
                HTTP_404_NOT_FOUND,
            )
        if action == "credit":
            found_account.balance += serializer.validated_data["balance"]

            current_extract, _ = Extract.objects.update_or_create(
                extract_account_id=account_id,
                defaults={"current_account_balance": found_account.balance},
            )

            transaction = {
                "transaction_type": "credit",
                "transaction_value": serializer.validated_data["balance"],
            }
            Transactions.objects.create(
                **transaction,
                transaction_account=found_account,
                transaction_extract=current_extract
            )

        if action == "debit":
            found_account.balance -= serializer.validated_data["balance"]
            # new_balance = found_account.balance - serializer.validated_data["balance"]

            current_extract, _ = Extract.objects.update_or_create(
                extract_account_id=account_id,
                defaults={"current_account_balance": found_account.balance},
            )

            transaction = {
                "transaction_type": "debit",
                "transaction_value": serializer.validated_data["balance"],
            }
            Transactions.objects.create(
                **transaction,
                transaction_account=found_account,
                transaction_extract=current_extract
            )
        found_account.save()
        serializer = AccountsSerializer(found_account)

        return Response(serializer.data, HTTP_200_OK)


class ExtractView(APIView):
    def get(self, _, account_id: None):
        extract = Extract.objects.get(extract_account_id=account_id)
        serializer = ExtractSerializer(extract)
        return Response(serializer.data)
