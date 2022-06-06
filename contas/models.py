from uuid import uuid4
from django.db import models


class Accounts(models.Model):
    account_id = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    account_owner = models.CharField(max_length=255)
    balance = models.FloatField(default=0.0)


class Extract(models.Model):
    extract_id = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    extract_date = models.DateTimeField(editable=False, auto_now=True)
    former_account_balance = models.FloatField()
    current_account_balance = models.FloatField()
    extract_account = models.ForeignKey(Accounts, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.former_account_balance = self.extract_account.balance
        super(Extract, self).save(*args, **kwargs)


class Transactions(models.Model):
    transaction_id = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    transaction_type = models.CharField(max_length=255)
    transaction_value = models.FloatField()
    transaction_date = models.DateTimeField(auto_now=True)
    transaction_description = models.CharField(max_length=255)
    transaction_account = models.ForeignKey(Accounts, on_delete=models.CASCADE)
    transaction_extract = models.ForeignKey(
        Extract, on_delete=models.CASCADE, related_name="transactions"
    )
