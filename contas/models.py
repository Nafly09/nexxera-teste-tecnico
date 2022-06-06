from uuid import uuid4
from django.db import models


class Accounts(models.Model):
    account_id = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    account_owner = models.CharField(max_length=255)
    balance = models.FloatField(default=0.0)


class Extracts(models.Model):
    extract_id = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    extract_date = models.DateTimeField(auto_now=True)
    accounts = models.ManyToManyField(Accounts, related_name="extracts")
