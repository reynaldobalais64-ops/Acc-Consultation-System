from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from sqlalchemy import func
from ..extensions import db
from ..models import Consultation, User, Announcement

admin_bp = Blueprint('admin', __name__)

@admin_bp.before_request
@login_required
def protect():
    if current_user.role != 'super_admin':
        return redirect(url_for('main.dashboard'))

@admin_bp.route('/dashboard')
def dashboard():
    stats = {
        'users': User.query.count(),
        'students': User.query.filter_by(role='student').count(),
        'experts': User.query.filter_by(role='medical_expert').count(),
        'pending': Consultation.query.filter_by(status='Pending').count(),
        'completed': Consultation.query.filter_by(status='Completed').count(),
    }
    recent = Consultation.query.order_by(Consultation.created_at.desc()).limit(8).all()
    return render_template('admin/dashboard.html', stats=stats, recent=recent)

@admin_bp.route('/users')
def users():
    return render_template('admin/users.html', users=User.query.order_by(User.created_at.desc()).all())

@admin_bp.route('/users/<int:user_id>/toggle', methods=['POST'])
def toggle_user(user_id):
    user = db.get_or_404(User, user_id)
    if user.id == current_user.id:
        flash('You cannot deactivate your own account.', 'danger')
    else:
        user.is_active_user = not user.is_active_user
        db.session.commit()
        flash('User status updated.', 'success')
    return redirect(url_for('admin.users'))

@admin_bp.route('/announcements', methods=['GET', 'POST'])
def announcements():
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()
        if title and content:
            db.session.add(Announcement(title=title, content=content))
            db.session.commit()
            flash('Announcement published.', 'success')
            return redirect(url_for('admin.announcements'))
        flash('Title and content are required.', 'danger')
    return render_template('admin/announcements.html', announcements=Announcement.query.order_by(Announcement.created_at.desc()).all())
