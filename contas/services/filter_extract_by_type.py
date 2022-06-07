def filter_extract_by_type(transaction_type, serializer):
    if transaction_type == "debit":
        only_debits = [
            dict(data)
            for data in serializer.data["transactions"]
            if data["transaction_type"] == "debit"
        ]
        serializer._data["transactions"] = only_debits
    if transaction_type == "credit":
        only_credits = [
            dict(data)
            for data in serializer.data["transactions"]
            if data["transaction_type"] == "credit"
        ]
        serializer._data["transactions"] = only_credits
