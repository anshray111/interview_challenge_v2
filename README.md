# AdviNow Interview Challenge

This project is built with **FastAPI**, **SQLAlchemy**, and **Alembic**, and includes a working API for:
- Importing business-symptom data from a CSV file
- Fetching filtered business-symptom relationships
- Health check endpoint
- API documentation

---

## Task Completion Overview

> Organized according to the original instructions, in the order they were completed:

1. **Create a virtual environment and install the requirements**
   - Used `requirements/requirements.txt` to install FastAPI, Alembic, SQLAlchemy, and others.

2. **Create data models - example with SQLAlchemy in `app/models.py`**
   - Created `Business`, `Symptom`, and `BusinessSymptom` tables.

3. **Design a database mockup based on `app/data/business_symptom_data.csv`**
   - Reviewed and mapped CSV fields to the models.

4. **Create an endpoint for importing a CSV file into the database**
   - Endpoint: `POST /import-csv`
   - Accepts `file` in `multipart/form-data`.

5. **Create an endpoint that returns business and symptom data**
    - Endpoint: `GET /symptoms`
    - Endpoint should take two optional parameters - `business_id` & `diagnostic`**
        - Both are query parameters in the `/symptoms` endpoint.
    - Endpoint should return Business ID, Business Name, Symptom Code, Symptom Name, and Symptom Diagnostic values based on filters**
        - Proper filtering using SQLAlchemy joins and conditionals.

6. **Generate migration script and run migration to create database tables - Alembic files provided**
   - Ran:
     ```bash
     alembic revision --autogenerate -m "Initial tables"
     alembic upgrade head
     ```

---

## Getting Started

### 1. Clone the repo and navigate into the project:
```bash
cd interview-challenge-v2
```

### 2. Create & activate a virtual environment:
```bash
python -m venv venv
venv\Scripts\activate    # On Windows
```

### 3. Install dependencies:
```bash
pip install -r requirements/requirements.txt
```

### 4. Set up your `.env` file:
Create a `.env` in the project root with:
```env
DB_HOST=localhost
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=your_password_here
```

### 5. Run Alembic migrations:
```bash
alembic revision --autogenerate -m "Initial tables"
alembic upgrade head
```

### 6. Start the FastAPI server:
```bash
python app/run.py
```

### 7. Access API Docs:
```
http://127.0.0.1:8013/docs
```

---

## Testing the API

### Health Check
```http
GET /status
```

### Import CSV
```http
POST /import-csv
Content-Type: multipart/form-data
Form Key: file (upload your CSV file)
```

### Get Filtered Symptoms
```http
GET /symptoms
Optional query params:
  - business_id
  - diagnostic
```
