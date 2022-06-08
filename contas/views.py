from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import APIView
from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_422_UNPROCESSABLE_ENTITY,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK,
)
from contas.services.update_extract_with_transaction import (
    update_extract_with_transaction,
)
from contas.services.filter_extract_by_type import filter_extract_by_type
from contas.models import Extract, Accounts
from contas.serializers import (
    AccountsSerializer,
    ExtractSerializer,
    UpdateAccountBalanceSerializer,
)


class AccountsView(APIView):
    def post(self, request: Request):
        try:
            serializer = AccountsSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            account = Accounts.objects.create(**serializer.validated_data)
            serializer = AccountsSerializer(account)
            return Response(serializer.data, HTTP_201_CREATED)
        except IntegrityError:
            return Response(
                {"message": "Requested account owner already exists"},
                HTTP_422_UNPROCESSABLE_ENTITY,
            )

    def get(self, _: Request):
        found_accounts = Accounts.objects.all()
        serializer = [AccountsSerializer(account).data for account in found_accounts]
        return Response(serializer)

    def patch(self, request: Request, action: None, account_id):
        try:
            serializer = UpdateAccountBalanceSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            found_account = Accounts.objects.get(account_id=account_id)
            update_extract_with_transaction(
                action, found_account, serializer, account_id
            )
            found_account.save()
            serializer = AccountsSerializer(found_account)

            return Response(serializer.data, HTTP_200_OK)
        except ValidationError:
            return Response(
                {"message": "Requested account_id is not a valid UUID"},
                HTTP_422_UNPROCESSABLE_ENTITY,
            )
        except Accounts.DoesNotExist:
            return Response(
                {"message": "Requested account_id does not exist"},
                HTTP_404_NOT_FOUND,
            )


class ExtractView(APIView):
    def get(self, request: Request, account_id: None):
        try:
            extract: Extract = Extract.objects.get(extract_account_id=account_id)
            serializer = ExtractSerializer(extract)
            transaction_type = request.GET.get("transaction_type")
            filter_extract_by_type(transaction_type, serializer)
            return Response(serializer.data)
        except ValidationError:
            return Response(
                {"message": "Requested account_id is not a valid UUID"},
                HTTP_422_UNPROCESSABLE_ENTITY,
            )
        except Extract.DoesNotExist:
            return Response(
                {"message": "Requested account_id does not exist"},
                HTTP_404_NOT_FOUND,
            )
