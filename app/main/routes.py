from flask import Blueprint, redirect, render_template, url_for
from flask_login import current_user, login_required
from ..models import Announcement

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('main/index.html', announcements=Announcement.query.order_by(Announcement.created_at.desc()).all())

@main_bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.role == 'student':
        return redirect(url_for('student.dashboard'))
    if current_user.role == 'medical_expert':
        return redirect(url_for('expert.dashboard'))
    return redirect(url_for('admin.dashboard'))
