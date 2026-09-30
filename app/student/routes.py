from datetime import date
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from ..extensions import db
from ..models import Consultation
from ..decorators import role_required

student_bp = Blueprint('student', __name__)

@student_bp.before_request
@login_required
def protect():
    if current_user.role != 'student':
        return redirect(url_for('main.dashboard'))

@student_bp.route('/dashboard')
def dashboard():
    consultations = Consultation.query.filter_by(student_id=current_user.id).order_by(Consultation.created_at.desc()).all()
    return render_template('student/dashboard.html', consultations=consultations)

@student_bp.route('/consultation/new', methods=['GET', 'POST'])
def new_consultation():
    if request.method == 'POST':
        concern = request.form.get('concern', '').strip()
        preferred_date = request.form.get('preferred_date', '')
        preferred_time = request.form.get('preferred_time', '').strip()
        if not concern or not preferred_date or not preferred_time:
            flash('Please complete all consultation fields.', 'danger')
        else:
            try:
                parsed_date = date.fromisoformat(preferred_date)
                if parsed_date < date.today():
                    raise ValueError
            except ValueError:
                flash('Please choose a valid future date.', 'danger')
                return render_template('student/new_consultation.html')
            consultation = Consultation(
                student_id=current_user.id,
                concern=concern,
                preferred_date=parsed_date,
                preferred_time=preferred_time,
            )
            db.session.add(consultation)
            db.session.commit()
            flash('Consultation request submitted.', 'success')
            return redirect(url_for('student.dashboard'))
    return render_template('student/new_consultation.html')

@student_bp.route('/consultation/<int:consultation_id>')
def view_consultation(consultation_id):
    consultation = db.get_or_404(Consultation, consultation_id)
    if consultation.student_id != current_user.id:
        return redirect(url_for('student.dashboard'))
    return render_template('student/view_consultation.html', consultation=consultation)
