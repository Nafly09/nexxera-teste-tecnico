from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import APIView
from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_401_UNAUTHORIZED,
    HTTP_403_FORBIDDEN,
    HTTP_422_UNPROCESSABLE_ENTITY,
)
from contas.models import Accounts
from contas.serializers import AccountsSerializer, ExtractSerializer


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
        serializer = AccountsSerializer(request.user)
        found_accounts = Accounts.objects.all()
        serializer = [AccountsSerializer(account).data for account in found_accounts]
        return Response(serializer)
