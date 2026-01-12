📘 UniAssist — Official University Rules Assistant

UniAssist is a document-driven AI-style assistant for universities that answers student queries only from official university documents (PDFs such as rules, policies, notices).

It allows administrators to upload/update rules and students to query them in natural language.

✨ Features

📄 Upload official university PDFs (rules, policies, notices)

🔄 Re-index knowledge instantly (no code changes needed)

💬 Chat interface for students

🎓 University-specific answers (no hallucinations)

🔐 Admin dashboard for document management

🧠 Keyword-based semantic search engine (no external APIs)

💻 Runs fully offline / locally

🏗️ Project Structure
uniassist/
├── backend/
│   ├── app.py               # Flask backend
│   ├── admin.py             # Admin upload & reindex routes
│   ├── search_engine.py     # Search logic
│   └── __init__.py
│
├── scripts/
│   ├── pdf_to_text.py       # PDF → text converter
│   └── chunk_text.py        # Text chunking logic
│
├── uploads/
│   └── bennett/             # Uploaded PDFs
│
├── text/
│   └── bennett/             # Extracted text files
│
├── processed/
│   └── bennett/
│       └── chunks.json      # Search index
│
├── frontend/
│   ├── index.html           # Landing page
│   ├── chat.html            # Chat UI
│   ├── admin.html           # Admin dashboard
│   ├── style.css
│   └── chat.js
│
└── README.md

🧰 Requirements
Python

Python 3.9+ (recommended)

Check:

python --version

📦 Install Dependencies
macOS / Linux
python3 -m pip install --user flask flask-cors pdfplumber scikit-learn

Windows (Command Prompt or PowerShell)
python -m pip install flask flask-cors pdfplumber scikit-learn

▶️ How to Run UniAssist
1️⃣ Start Backend Server
cd backend
python app.py


You should see:

Running on http://127.0.0.1:5000


⚠️ Keep this terminal open.

2️⃣ Open Frontend

Open the file directly in your browser:

frontend/index.html


(or double-click it)

🔐 Admin Dashboard

Open:

frontend/admin.html


Default admin password:

admin123

Admin can:

Upload new PDF documents

Re-index the knowledge base instantly

🧪 Example Questions

Try asking:

What is a day out pass?
Do I need warden approval for leave out pass?
What happens if attendance is below 75%?
How do I apply for supplementary exam?


Answers are generated only from uploaded official documents.

🛡️ Important Notes

This project does not use OpenAI / Gemini / external APIs

All answers are document-grounded

Ideal for:

Universities

Colleges

Internal policy assistants

🚀 Roadmap

Document enable/disable controls

Admin analytics dashboard

Multi-university support

Secure admin authentication

Deployment-ready version

📄 License

This project is currently intended for educational and internal institutional use.
License can be customized for commercial deployment.

🙌 Author

Built by Aditya Sinha
Project: UniAssist
