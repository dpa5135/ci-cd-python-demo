"""Tiny educational transaction-risk classifier. Not a real AML model."""

THRESHOLD = 20_000


def classify_transaction(amount):
    """Return a simple risk label for a nonnegative transaction amount."""
    if not isinstance(amount, (int, float)) or isinstance(amount, bool):
        raise TypeError("amount must be a number")
    if amount < 0:
        raise ValueError("amount cannot be negative")
    return "High Risk" if amount > THRESHOLD else "Low Risk"
