## 📘 Шаг 1: Структура `README.md`


1. **Project Description**
2. **Tech Stack**
3. **Installation**
4. **Environment Variables**
5. **API Overview**
6. **Endpoints**


---

# 📱 Referral System API

A simple referral system built with Django, Django REST Framework, and PostgreSQL.

Users can authenticate via phone number, receive a simulated 4-digit code, and activate invite codes.
 

---

  

## 🚀 Tech Stack

- Python 3.x
- Django
- Django REST Framework
- PostgreSQL
- SimpleJWT for token authentication

---

## 🛠️ Installation


Clone the repository and create a virtual environment:

```bash

git clone <your_repo_url>

cd referral_project

python -m venv venv

source venv/bin/activate

pip install -r requirements.txt

````

---

## ⚙️ Environment Variables  

Create a `.env` file in the root directory:

```
DB_NAME=referral_db
DB_USER=postgres
DB_PASSWORD=password
DB_HOST=localhost
DB_PORT=5432
```

---

## 🔧 Apply Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

---

## ▶️ Run the Server  

```bash
python manage.py runserver
```

---
## 🔐 API Overview

The authentication flow is based on phone numbers and simulated SMS codes.
No passwords required — just phone number and verification code.

---
## 🔌 Endpoints

### 1. Send Code

`POST /api/send-code/`

```json
{
"phone_number": "79991112233"
}
```

---
### 2. Verify Code and Get Token

`POST /api/verify-code/`

```json
{
"phone_number": "79991112233",
"code": "1234"
}
```

✅ Returns `access` and `refresh` tokens + invite code.

---
### 3. Get Profile

`GET /api/profile/`

Requires JWT Access Token 

**Headers:**

```

Authorization: Bearer <access_token>

```

---
### 4. Activate Invite Code

`POST /api/profile/activate/`

Requires JWT Access Token

```json
{
"code": "ABC123"
}
```
