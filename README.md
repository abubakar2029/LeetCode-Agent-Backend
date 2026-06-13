# ⚙️ LeetCode Agent – Backend

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green?logo=fastapi)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-ORM-red)

## 🚀 Overview

FastAPI backend for the **LeetCode Agent Chrome Extension**. Handles GitHub OAuth, user sessions, and repository linking so the extension can track LeetCode progress.

- **Backend (this repo)** – Auth, GitHub integration, and user data APIs.
- **Frontend** – Chrome extension UI built with React, Vite, and Tailwind.
  👉 [LeetCode Agent Frontend](https://github.com/abubakar2029/LeetCode-Agent-UI)

---

## 🛠️ Tech Stack

- **FastAPI**
- **SQLAlchemy** (SQLite)
- **PyJWT** (session tokens)
- **Cryptography** (encrypted GitHub tokens)

---

## 📂 Project Structure

```
backend/
├── app/
│   ├── routers/        # API routes (auth, github)
│   ├── services/       # GitHub & database logic
│   ├── utils/          # Security & auth helpers
│   ├── main.py         # App entry point
│   ├── models.py       # Database models
│   └── database.py     # DB configuration
├── requirements.txt
└── README.md
```

---

## ⚙️ Setup & Installation

### 1. Clone the repo

```bash
git clone https://github.com/abubakar2029/LeetCode-Agent.git
cd LeetCode-Agent
```

### 2. Create a virtual environment

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # macOS / Linux
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
GITHUB_CLIENT_ID=your_github_client_id
GITHUB_CLIENT_SECRET=your_github_client_secret
JWT_SECRET=your_jwt_secret
JWT_ALGORITHM=HS256
ENCRYPTION_KEY=your_fernet_key
EXTENSION_REDIRECT=your_chrome_extension_id
```

Set the GitHub OAuth callback URL to `http://localhost:8000/auth/callback`.

### 5. Run the server

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

API docs: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 📌 Features

- 🔐 GitHub OAuth for Chrome extension login
- 🐙 List and link a user's GitHub repository
- 🔒 Encrypted storage of GitHub access tokens
- 🎫 JWT-based authenticated API access

---

## 📡 API Routes

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/auth/login` | Start GitHub OAuth flow |
| `GET` | `/auth/callback` | OAuth callback |
| `GET` | `/auth/get-public-repo` | List user repos (auth required) |
| `POST` | `/auth/confirm-repo` | Link selected repo (auth required) |

---

## 🤝 Contributing

1. Fork the repo
2. Create a branch: `git checkout -b feature-name`
3. Commit changes: `git commit -m "Add feature"`
4. Push: `git push origin feature-name`
5. Open a Pull Request

---

## 📜 License

MIT License © 2025 LeetCode Agent Team
