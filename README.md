# Abuyog Community College Consultation System

A role-based consultation management system built with Python Flask, Jinja2/HTML/CSS, SQLite, SQLAlchemy, and Flask-Login.

## Roles

- **Super Admin** — dashboard, user activation/deactivation, announcements, system overview.
- **Medical Expert** — consultation queue, assign self, update status, add expert notes.
- **Student** — registration, consultation request, request tracking, consultation details.

## Technology

- Python 3.11+
- Flask 3.1
- Flask-SQLAlchemy
- Flask-Login
- SQLite
- HTML5 + Jinja2
- CSS3
- Primary UI color: `#C23C47`

## 1. Open the project

Extract the project folder and open a terminal in:

```text
acc_consultation_system/
```

## 2. Create a virtual environment

### Windows PowerShell

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, run:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then activate again.

### Windows CMD

```cmd
py -m venv .venv
.venv\Scripts\activate
```

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

## 4. Run the system

```bash
python run.py
```

Open:

`http://127.0.0.1:5000`

The SQLite database is created automatically at:

`app/instance/acc_consultation.db`

## 5. Demo accounts

| Role | Username | Password |
|---|---|---|
| Super Admin | `admin` | `Admin@123` |
| Medical Expert | `expert` | `Expert@123` |
| Student | `student` | `Student@123` |

Change these credentials before using the application outside a classroom/demo environment.

## 6. Main workflow

1. A student registers or signs in.
2. Student submits a consultation request with concern, preferred date, and preferred time.
3. The request starts as **Pending**.
4. A medical expert sees the request in the expert queue.
5. The medical expert can update it to **Approved**, **Completed**, or **Cancelled**, and add notes.
6. The student can see the current status and notes.
7. The super admin monitors users and consultation statistics.
8. The super admin can publish announcements displayed on the public landing page.

## Architecture

```text
acc_consultation_system/
├── app/
│   ├── __init__.py          # Application factory
│   ├── decorators.py        # RBAC helper
│   ├── extensions.py        # SQLAlchemy + LoginManager
│   ├── models.py            # User, Consultation, Announcement
│   ├── seed.py              # Demo data
│   ├── auth/routes.py       # Login, register, logout
│   ├── main/routes.py       # Public pages + dashboard redirect
│   ├── student/routes.py    # Student workflow
│   ├── expert/routes.py     # Medical expert workflow
│   ├── admin/routes.py      # Super admin workflow
│   ├── templates/           # Jinja2 HTML
│   └── static/css/          # UI styles
├── instance/                # Runtime database directory
├── config.py
├── requirements.txt
├── run.py
└── README.md
```

## RBAC rules

The application checks the authenticated user's role before entering protected role routes. Students cannot access expert/admin pages, experts cannot access admin pages, and only super admins can manage users and announcements.

## Resetting the demo database

Stop Flask, delete:

```text
app/instance/acc_consultation.db
```

Then run `python run.py` again. The database and demo accounts will be recreated.

## Production hardening checklist

Before production deployment, set a strong random `SECRET_KEY`, disable Flask debug mode, add CSRF protection (for example Flask-WTF), add audit logging, add database migrations with Alembic/Flask-Migrate, enforce stronger password policy, add email verification/password reset, and use a production WSGI server.
