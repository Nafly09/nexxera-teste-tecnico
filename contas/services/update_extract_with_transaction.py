from contas.models import Extract, Transactions


def update_extract_with_transaction(
    transaction_type, found_account, serializer, account_id
):
    if transaction_type == "credit":
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

    if transaction_type == "debit":
        found_account.balance -= serializer.validated_data["balance"]
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
