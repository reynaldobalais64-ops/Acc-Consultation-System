from .extensions import db
from .models import User, Announcement


def seed_database():
    changed = False
    accounts = [
        ('Super Admin', 'admin', 'admin@acc.edu.ph', 'Admin@123', 'super_admin'),
        ('Dr. Maria Santos', 'expert', 'expert@acc.edu.ph', 'Expert@123', 'medical_expert'),
        ('Juan Dela Cruz', 'student', 'student@acc.edu.ph', 'Student@123', 'student'),
    ]
    for full_name, username, email, password, role in accounts:
        if not User.query.filter_by(username=username).first():
            user = User(full_name=full_name, username=username, email=email, role=role)
            user.set_password(password)
            db.session.add(user)
            changed = True

    if not Announcement.query.first():
        db.session.add(Announcement(
            title='Welcome to ACC Consultation System',
            content='Students may submit consultation requests online. Medical experts can review and respond to requests.',
        ))
        changed = True
    if changed:
        db.session.commit()
