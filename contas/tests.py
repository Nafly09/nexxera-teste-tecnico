from django.test import TestCase
from rest_framework.test import APITestCase

from contas.models import Accounts


class AccountsModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.account_owner = "John"
        cls.balance = 0.0

        cls.account = Accounts.objects.create(account_owner=cls.account_owner)

    def test_account_has_information_fields(self):

        self.assertIsInstance(self.account.account_owner, str)
        self.assertEqual(self.account.account_owner, self.account_owner)

        self.assertIsInstance(self.account.balance, float)
        self.assertEqual(self.account.balance, self.balance)


class AccountsViewTest(APITestCase):
    def test_can_create_a_new_account(self):
        url_create = f"/api/accounts/"
        payload = {"account_owner": "Jane Doe", "balance": 2000}

        response = self.client.post(url_create, payload)

        created_account = Accounts.objects.get(account_owner=payload["account_owner"])

        self.assertEquals(201, response.status_code)

        for key, value in payload.items():
            self.assertEquals(value, response.data[key])
            self.assertEquals(value, getattr(created_account, key))

    def test_can_create_a_new_transaction(self):
        url_create_test_account = f"/api/accounts/"
        test_account_payload = {"account_owner": "Jane Doe", "balance": 2000}
        account_creation_response = self.client.post(
            url_create_test_account, test_account_payload
        )
        test_account_id = account_creation_response.data["account_id"]

        url_create_credit_transaction = f"/api/accounts/credit/{test_account_id}/"
        credit_transaction_payload = {"balance": 100}
        credit_transaction_response = self.client.patch(
            url_create_credit_transaction, credit_transaction_payload
        )
        self.assertEquals(200, credit_transaction_response.status_code)

        url_create_debit_transaction = f"/api/accounts/debit/{test_account_id}/"
        debit_transaction_payload = {"balance": 100}
        debit_transaction_response = self.client.patch(
            url_create_debit_transaction, debit_transaction_payload
        )
        self.assertEquals(200, debit_transaction_response.status_code)

    def test_cannot_create_new_transaction_with_invalid_id(self):
        url_create_test_account = f"/api/accounts/"
        test_account_payload = {"account_owner": "Jane Doe", "balance": 2000}
        self.client.post(url_create_test_account, test_account_payload)
        test_account_id = "7998875a-cc38-47dc-882a-7ff95a419532"

        url_create_credit_transaction = f"/api/accounts/credit/{test_account_id}/"
        credit_transaction_payload = {"balance": 100}
        credit_transaction_response = self.client.patch(
            url_create_credit_transaction, credit_transaction_payload
        )
        self.assertEquals(404, credit_transaction_response.status_code)
        self.assertEquals(
            {"message": "Requested account_id does not exist"},
            credit_transaction_response.data,
        )

    def test_cannot_create_new_transaction_with_invalid_UUID_type_ID(self):
        url_create_test_account = f"/api/accounts/"
        test_account_payload = {"account_owner": "Jane Doe", "balance": 2000}
        self.client.post(url_create_test_account, test_account_payload)
        test_account_id = "ahsuahsuahsuah"

        url_create_credit_transaction = f"/api/accounts/credit/{test_account_id}/"
        credit_transaction_payload = {"balance": 100}
        credit_transaction_response = self.client.patch(
            url_create_credit_transaction, credit_transaction_payload
        )
        self.assertEquals(422, credit_transaction_response.status_code)
        self.assertEquals(
            {"message": "Requested account_id is not a valid UUID"},
            credit_transaction_response.data,
        )

    def test_can_retrieve_all_accounts(self):
        mock_account_data = [
            {"account_owner": "John Doe", "balance": 2000},
            {"account_owner": "Jane Doe", "balance": 2000},
            {"account_owner": "Joseph Joestar", "balance": 2000},
            {"account_owner": "Jonathan Joestar", "balance": 2000},
            {"account_owner": "Naruto Uzumaki", "balance": 2000},
        ]
        mock_accounts = [
            self.client.post("/api/accounts/", payload).data
            for payload in mock_account_data
        ]

        url_retrieve = f"/api/accounts/"
        retrieve_accounts_response = self.client.get(url_retrieve)
        self.assertEquals(200, retrieve_accounts_response.status_code)
        self.assertEquals(mock_accounts, retrieve_accounts_response.data)

    def test_cannot_create_an_account_with_a_duplicate_owner_name(self):
        url_create_test_account = f"/api/accounts/"
        test_account_payload = {"account_owner": "Jane Doe", "balance": 2000}
        self.client.post(url_create_test_account, test_account_payload)
        duplicate_account_creation_response = self.client.post(
            url_create_test_account, test_account_payload
        )

        self.assertEquals(422, duplicate_account_creation_response.status_code)
        self.assertEquals(
            {"message": "Requested account owner already exists"},
            duplicate_account_creation_response.data,
        )

    def test_can_retrieve_a_valid_extract(self):
        url_create_test_account = f"/api/accounts/"
        test_account_payload = {"account_owner": "Jane Doe", "balance": 2000}
        account_creation_response = self.client.post(
            url_create_test_account, test_account_payload
        )
        test_account_id = account_creation_response.data["account_id"]

        url_create_credit_transaction = f"/api/accounts/credit/{test_account_id}/"
        credit_transaction_payload = {"balance": 100}
        [
            self.client.patch(url_create_credit_transaction, credit_transaction_payload)
            for _ in range(30)
        ]
        url_retrieve_extract = f"/api/extracts/{test_account_id}/"

        response = self.client.get(url_retrieve_extract)

        self.assertEquals(200, response.status_code)

    def test_cannot_retrieve_extract_with_invalid_UUID_type_ID(self):
        url_create_test_account = f"/api/accounts/"
        test_account_payload = {"account_owner": "Jane Doe", "balance": 2000}
        self.client.post(url_create_test_account, test_account_payload)
        test_account_id = "ajhsauhsahsauhs"

        url_create_credit_transaction = f"/api/accounts/credit/{test_account_id}/"
        credit_transaction_payload = {"balance": 100}
        self.client.patch(url_create_credit_transaction, credit_transaction_payload)
        url_retrieve_extract = f"/api/extracts/{test_account_id}/"

        response = self.client.get(url_retrieve_extract)

        self.assertEquals(422, response.status_code)
        self.assertEquals(
            {"message": "Requested account_id is not a valid UUID"}, response.data
        )

    def test_cannot_retrieve_extract_with_invalid_ID(self):
        url_create_test_account = f"/api/accounts/"
        test_account_payload = {"account_owner": "Jane Doe", "balance": 2000}
        self.client.post(url_create_test_account, test_account_payload)
        test_account_id = "7998875a-cc38-47dc-882a-7ff95a419532"

        url_create_credit_transaction = f"/api/accounts/credit/{test_account_id}/"
        credit_transaction_payload = {"balance": 100}
        self.client.patch(url_create_credit_transaction, credit_transaction_payload)
        url_retrieve_extract = f"/api/extracts/{test_account_id}/"

        response = self.client.get(url_retrieve_extract)

        self.assertEquals(404, response.status_code)
        self.assertEquals(
            {"message": "Requested account_id does not exist"}, response.data
        )

    def test_filter_extracts_by_debit_type(self):
        url_create_test_account = f"/api/accounts/"
        test_account_payload = {"account_owner": "Jane Doe", "balance": 2000}
        account_creation_response = self.client.post(
            url_create_test_account, test_account_payload
        )
        test_account_id = account_creation_response.data["account_id"]

        url_create_credit_transaction = f"/api/accounts/credit/{test_account_id}/"
        credit_transaction_payload = {"balance": 100}
        self.client.patch(url_create_credit_transaction, credit_transaction_payload)

        url_create_debit_transaction = f"/api/accounts/debit/{test_account_id}/"
        debit_transaction_payload = {"balance": 100}
        self.client.patch(url_create_debit_transaction, debit_transaction_payload)

        url_retrieve_extract = f"/api/extracts/{test_account_id}/"
        response = self.client.get(url_retrieve_extract, {"transaction_type": "debit"})

        extract_types = [
            transaction_type for transaction_type in response.data["transactions"]
        ]

        self.assertEqual(200, response.status_code)
        for current_type in extract_types:
            self.assertEquals(current_type["transaction_type"], "debit")

    def test_filter_extracts_by_credit_type(self):
        url_create_test_account = f"/api/accounts/"
        test_account_payload = {"account_owner": "Jane Doe", "balance": 2000}
        account_creation_response = self.client.post(
            url_create_test_account, test_account_payload
        )
        test_account_id = account_creation_response.data["account_id"]

        url_create_credit_transaction = f"/api/accounts/credit/{test_account_id}/"
        credit_transaction_payload = {"balance": 100}
        self.client.patch(url_create_credit_transaction, credit_transaction_payload)

        url_create_debit_transaction = f"/api/accounts/debit/{test_account_id}/"
        debit_transaction_payload = {"balance": 100}
        self.client.patch(url_create_debit_transaction, debit_transaction_payload)

        url_retrieve_extract = f"/api/extracts/{test_account_id}/"
        response = self.client.get(url_retrieve_extract, {"transaction_type": "credit"})

        extract_types = [
            transaction_type for transaction_type in response.data["transactions"]
        ]

        self.assertEqual(200, response.status_code)
        for current_type in extract_types:
            self.assertEquals(current_type["transaction_type"], "credit")
