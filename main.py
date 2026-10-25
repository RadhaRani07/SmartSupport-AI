
import ollama

print("===== SmartSupport AI =====")

ticket = input("Enter customer complaint: ").strip()

if not ticket:
    print("Please enter a customer complaint.")

else:
    prompt = f"""
You are SmartSupport AI, a customer support ticket analysis assistant.

Customer complaint:
{ticket}

Return these fields:
Category:
Assigned Team:
Priority: High, Medium, or Normal
Reason:
Suggested Customer Reply:

Routing rules:
- Payment, billing, double charges, and refunds: Billing and Refund; Billing Team.
- Login, password, or account access: Account Access; Technical Support.
- Order status, shipping, or delivery without a billing issue: Order and Delivery; Order Support.
- Other issues: General Support; Customer Support.
- Billing and refund issues take priority over order and delivery.

Priority rules:
- High: Explicitly urgent or serious service disruption.
- Medium: A specific request for help without explicit urgency.
- Normal: Routine questions.

Reply rules:
- Be polite and professional.
- Never claim a refund has been approved, started, or completed.
- Never promise a resolution time.
- Do not invent customer names or company details.
- Say the relevant team can review the issue.
- End with Customer Support Team.
"""

    try:
        response = ollama.chat(
            model="qwen2.5:3b",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        analysis = response["message"]["content"]

        print("\n===== AI Ticket Analysis =====")
        print(analysis)

        print("\n===== Human Approval =====")
        print("1. Approve")
        print("2. Reject")

        decision = input("Choose 1 or 2: ").strip()

        if decision == "1":
            print("\nStatus: Approved by human reviewer")
            print("The suggested reply is approved for review/use.")

        elif decision == "2":
            print("\nStatus: Rejected by human reviewer")
            print("The suggested reply needs revision.")

        else:
            print("\nStatus: Pending human approval")
            print("Invalid choice. Please run the program again.")

    except Exception as error:
        print("\nAI request failed.")
        print("Check that Ollama is running and try again.")
        print("Error:", error)