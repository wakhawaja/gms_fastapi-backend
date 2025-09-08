# FastAPI Backend

A backend service built with **FastAPI**, **MongoDB**, and **JWT authentication**, managed with [uv](https://github.com/astral-sh/uv).

---

## 🚀 Features
- FastAPI server with async MongoDB (Motor)
- JWT authentication (`python-jose`, `bcrypt`)
- Health checks (`/api/health`, `/api/db-health`)
- CORS enabled for frontend (default: `http://localhost:3000`)
- Environment-based config with `.env`

---

## 🛠️ Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/wakhawaja/fastapi-backend.git
cd fastapi-backend
