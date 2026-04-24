# CPDCL Backend (FastAPI)

A backend service built using **FastAPI**.

---

##  Project Setup

### 1. Clone the repository

```bash
git clone https://github.com/indrasenareddy3/cpdcl_backend.git
cd cpdcl_backend
```

---

##  Create & Activate Virtual Environment

### Windows (PowerShell)

```bash
python -m venv venv
venv\Scripts\activate
```

### Windows (CMD)

```bash
python -m venv venv
venv\Scripts\activate.bat
```

### Linux / Mac

```bash
python3 -m venv venv
source venv/bin/activate
```

---

##  Install Dependencies

```bash
pip install -r requirements.txt
```

---

##  Environment Variables

Create a `.env` file in the root directory and configure required variables:

```env
DATABASE_URL=your_database_url
SECRET_KEY=your_secret_key
```

---

## Database Migrations (Alembic)

### Initialize migrations (first time only)

```bash
alembic init alembic
```

### Create a migration

```bash
alembic revision --autogenerate -m "initial migration"
```

### Apply migrations

```bash
alembic upgrade head
```

### Rollback (if needed)

```bash
alembic downgrade -1
```

---

##  Run the FastAPI Server

```bash
uvicorn app.main:app --reload
```

* App will run at: http://127.0.0.1:8000
* Swagger docs: http://127.0.0.1:8000/docs

---

##  Docker Setup

### 1. Build Docker Image

```bash
docker build -t cpdcl-backend .
```

### 2. Run Docker Container

```bash
docker run -d -p 8000:8000 cpdcl-backend
```

---

## Project Structure (Example)

```
cpdcl_backend/
│── app/
│   ├── main.py
│   ├── models/
│   ├── routes/
│   ├── schemas/
│── alembic/
│── requirements.txt
│── Dockerfile
│── README.md
```


## Tech Stack

* FastAPI
* SQLAlchemy
* Alembic
* Uvicorn
* Docker