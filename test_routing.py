import unittest
from routing import expected_team, validate_analysis


class TestSmartSupportRouting(unittest.TestCase):

    def test_billing_complaint(self):
        team, category = expected_team(
            "My payment was deducted twice."
        )
        self.assertEqual(team, "Billing Team")
        self.assertEqual(category, "Billing and Refund")

    def test_delivery_complaint(self):
        team, category = expected_team(
            "My order has not been delivered yet."
        )
        self.assertEqual(team, "Order Support")
        self.assertEqual(category, "Order and Delivery")

    def test_account_access_complaint(self):
        team, category = expected_team(
            "I cannot access my account."
        )
        self.assertEqual(team, "Technical Support")
        self.assertEqual(category, "Account Access")

    def test_general_complaint(self):
        team, category = expected_team(
            "I have a question about your service."
        )
        self.assertEqual(team, "Customer Support")
        self.assertEqual(category, "General Support")

    def test_billing_takes_priority_over_delivery(self):
        team, category = expected_team(
            "My order is late and I was charged twice."
        )
        self.assertEqual(team, "Billing Team")
        self.assertEqual(category, "Billing and Refund")

    def test_valid_analysis_passes_validation(self):
        complaint = "My payment was deducted twice."

        analysis = """
Category: Billing and Refund
Assigned Team: Billing Team
Priority: High
Reason: The customer reports a duplicate payment.
Suggested Customer Reply: Hello,

Thank you for contacting us about the duplicate payment.
"""

        result = validate_analysis(complaint, analysis)
        self.assertEqual(result["issues"], [])

    def test_wrong_team_is_detected(self):
        complaint = "My payment was deducted twice."

        analysis = """
Category: Billing and Refund
Assigned Team: Order Support
Priority: High
Reason: Duplicate payment reported.
Suggested Customer Reply: Hello,
"""

        result = validate_analysis(complaint, analysis)
        self.assertTrue(
            any("Team mismatch" in issue for issue in result["issues"])
        )

    def test_invalid_priority_is_detected(self):
        complaint = "My payment was deducted twice."

        analysis = """
Category: Billing and Refund
Assigned Team: Billing Team
Priority: Urgent
Reason: Duplicate payment reported.
Suggested Customer Reply: Hello,
"""

        result = validate_analysis(complaint, analysis)
        self.assertTrue(
            any("Invalid priority" in issue for issue in result["issues"])
        )

    def test_wrong_category_is_detected(self):
        complaint = "My payment was deducted twice."

        analysis = """
Category: Order and Delivery
Assigned Team: Billing Team
Priority: High
Reason: Duplicate payment reported.
Suggested Customer Reply: Hello,
"""

        result = validate_analysis(complaint, analysis)
        self.assertTrue(
            any("Category mismatch" in issue for issue in result["issues"])
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)