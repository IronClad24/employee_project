# Employee Management API

This project is a backend system I built as a style exercise to manage employees, departments, attendance, and performance with production-ready engineering standards. It uses Django REST Framework, PostgreSQL, role-based authentication, and supports containerized deployment with Docker.

---

## 🚀 Features I Implemented

* Modular apps for Employee, Department, Attendance, and Performance
* DRF Token-based Authentication with role-based access (Admin, HR, Employee)
* Auto-token creation on user signup
* Filtering, searching, ordering for optimized API queries
* Cursor-based pagination for scalability
* Swagger integration for full API exploration
* Optional Chart.js dashboard for analytics
* Dockerfile and Docker Compose for consistent deployment
* Seed command using Faker to quickly bootstrap data

---

## 🏗️ Project Structure

```
employee_project/
├── employees/              # Employee & Department logic
├── attendance/             # Tracks attendance records
├── templates/              # Charts template
├── employee_project/       # Settings and URL routing
├── requirements.txt
├── .env.example
├── Dockerfile
├── docker-compose.yml
└── README.md
```

---

## 🔧 Local Setup

### 1. Clone the repo

```bash
git clone <repo-url>
cd employee_project
```

### 2. Setup virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure your environment

```bash
cp .env.example .env
# Fill in your DB credentials
```

> 🔑 To generate a new Django SECRET\_KEY:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

> 📌 Paste it into your `.env` like:

```env
SECRET_KEY=django-generated-secret-key-here
```

---

## 🗄️ PostgreSQL Setup (Local)

1. **Install PostgreSQL** (if not already): [https://www.postgresql.org/download/](https://www.postgresql.org/download/)
2. **Create database & user**:

```sql
CREATE DATABASE employee_db;
CREATE USER django_user WITH PASSWORD 'yourpassword';
ALTER ROLE django_user SET client_encoding TO 'utf8';
ALTER ROLE django_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE django_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE employee_db TO django_user;
```

3. **Set in `.env`**:

```
DEBUG=True
DATABASE_URL=postgres://django_user:yourpassword@localhost:5432/employee_db
SECRET_KEY=your_generated_secret_key
```

### 5. Run migrations and seed data

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py seed_data
```

### 6. Start the dev server

```bash
python manage.py runserver
```

---

## 🐳 Docker Setup

For isolated, production-like environments:

```bash
docker-compose up --build
```

To seed data in Docker:

```bash
docker-compose exec web python manage.py seed_data
```

---

## 🔐 Authentication Flow

* Obtain token: `POST /api/token/`
* Include header: `Authorization: Token <your_token>`

---

## 🧪 Unit Testing

All major modules are covered with API tests. Run:

```bash
python manage.py test
```

---

## 📊 Charts (Optional Visualization)

* Accessible at `/api/charts/`
* **Pie Chart**: Employee count per Department
* **Bar Chart**: Monthly Attendance Summary

---

## 📚 API Documentation

* Swagger UI: [http://localhost:8000/swagger/](http://localhost:8000/swagger/)

---

## ✅ Role Permissions

| Role     | Privileges                        |
| -------- | --------------------------------- |
| Admin    | Full access + user registration   |
| HR       | Manage employees & view analytics |
| Employee | View own data + attendance chart  |

---

## 📦 Deployment Considerations

* `DEBUG=False` for production
* Set `ALLOWED_HOSTS` properly
* Ensure `.env` has production `DATABASE_URL` & `SECRET_KEY`
* Use gunicorn for WSGI
* Ideal for Render, Railway, or Vercel (with container support)

---

## ✉️ Maintained By

Aryan Yadav — Built as part of a full-stack backend assignment, designed with scalable architecture and production readiness in mind.

Open to feedback and contributions.
