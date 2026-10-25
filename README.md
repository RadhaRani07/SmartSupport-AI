# SmartSupport AI
### AI-Powered Customer Support Ticket Management System

SmartSupport AI is an AI-powered customer support tool that analyzes customer complaints, categorizes tickets, assigns them to the appropriate support team, suggests priority levels, and drafts customer replies.

The project includes validation checks and a human approval workflow to help keep AI-generated decisions under review.

## Key Features

- **AI Ticket Analysis:** Analyzes customer complaints using a locally running language model.
- **Automatic Categorization:** Classifies tickets into categories such as Billing and Refund, Order and Delivery, Account Access, and General Support.
- **Team Routing:** Recommends the appropriate support team.
- **Priority Assessment:** Suggests High, Medium, or Normal priority.
- **Suggested Customer Replies:** Drafts replies for support staff to review.
- **Validation Checks:** Checks AI-generated results before approval.
- **Human-in-the-Loop Workflow:** Allows a human to review and approve or reject ticket handling.
- **SQLite Database:** Stores ticket records for persistent history.
- **Streamlit Dashboard:** Provides a simple interface for analyzing and reviewing tickets.

## Technology Stack

- Python
- Streamlit
- Ollama
- Qwen 2.5 (3B) language model
- SQLite
- Git and GitHub

## How It Works

1. A support agent enters a customer complaint.
2. The AI analyzes the complaint.
3. The system suggests a category, team, priority, reason, and customer reply.
4. Validation checks review the AI-generated analysis.
5. A human reviews the result and makes an approval decision.
6. Ticket records are stored in the database.

**Note:** Customer replies are drafted for review. They are not automatically sent to customers.

## Getting Started

### Prerequisites

- Python installed on your computer
- Ollama installed and running
- Git installed

### Installation

Clone the repository:

```bash
git clone https://github.com/RadhaRani07/SmartSupport-AI.git
cd SmartSupport-AI
```

Create and activate a virtual environment on Windows:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

Install the Python dependencies:

```bash
pip install -r requirements.txt
```

Download the required Ollama model:

```bash
ollama pull qwen2.5:3b
```

Run the Streamlit application:

```bash
streamlit run app.py
```

## Project Structure

```text
SmartSupport-AI/
├── app.py
├── database.py
├── main.py
├── test_ai.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Learning Outcomes

This project demonstrates practical work with:

- Local Large Language Models (LLMs)
- AI-assisted text classification
- Workflow automation
- Input and output validation
- Human-in-the-loop AI systems
- Database integration
- Interactive dashboards
- Version control with Git and GitHub

## Future Improvements

- Add automated tests for ticket classification and routing.
- Improve validation and error handling.
- Add ticket analytics and reporting.
- Deploy a demo application online.
- Add more robust logging and monitoring.

## Developer

Developed as a practical AI and Python portfolio project.
