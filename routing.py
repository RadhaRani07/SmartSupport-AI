
import re


def extract_field(analysis, field):
    pattern = rf"^\s*{re.escape(field)}\s*:\s*(.*?)(?=\n\s*[\w ]+\s*:|\Z)"
    match = re.search(pattern, analysis, re.IGNORECASE | re.MULTILINE | re.DOTALL)
    return match.group(1).strip() if match else "Not provided"


def expected_team(ticket_text):
    text = ticket_text.lower()

    billing_terms = [
        "refund", "billing", "paid twice", "paid two times",
        "double payment", "charged twice", "charged two times",
        "duplicate payment", "payment deducted", "deducted twice",
        "deducted two times", "payment was deducted twice",
        "payment was deducted two times", "payment issue",
        "overcharged", "charged more than once",
        "money deducted twice", "money was deducted twice",
        "payment taken twice", "paid for my order",
    ]

    login_terms = [
        "login", "log in", "password", "account access",
        "can't access", "cannot access", "unable to access",
        "locked out",
    ]

    delivery_terms = [
        "delivery", "shipping", "tracking", "order status",
        "not delivered", "not been delivered", "undelivered",
        "hasn't arrived", "has not arrived", "late order",
        "order has not arrived", "missing order",
    ]

    if any(term in text for term in billing_terms):
        return "Billing Team", "Billing and Refund"

    if any(term in text for term in login_terms):
        return "Technical Support", "Account Access"

    if any(term in text for term in delivery_terms):
        return "Order Support", "Order and Delivery"

    return "Customer Support", "General Support"


def validate_analysis(ticket_text, analysis):
    expected, expected_category = expected_team(ticket_text)

    category = extract_field(analysis, "Category")
    assigned = extract_field(analysis, "Assigned Team")
    priority = extract_field(analysis, "Priority")

    priority = priority.splitlines()[0].strip() if priority else "Not provided"

    valid_priorities = {
        "high": "High",
        "medium": "Medium",
        "normal": "Normal",
    }

    normalized_priority = valid_priorities.get(priority.casefold())
    issues = []

    if assigned.casefold() != expected.casefold():
        issues.append(
            f"Team mismatch: expected {expected}, but AI returned {assigned}."
        )

    if normalized_priority is None:
        issues.append(f"Invalid priority returned by AI: {priority}")

    if category.casefold() != expected_category.casefold():
        issues.append(
            f"Category mismatch: expected {expected_category}, but AI returned {category}."
        )

    return {
        "expected_team": expected,
        "expected_category": expected_category,
        "category": category,
        "assigned_team": assigned,
        "priority": normalized_priority or priority,
        "issues": issues,
    }
