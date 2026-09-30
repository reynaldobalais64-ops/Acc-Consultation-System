from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from ..extensions import db
from ..models import Consultation, User

expert_bp = Blueprint('expert', __name__)

@expert_bp.before_request
@login_required
def protect():
    if current_user.role != 'medical_expert':
        return redirect(url_for('main.dashboard'))

@expert_bp.route('/dashboard')
def dashboard():
    consultations = Consultation.query.order_by(Consultation.created_at.desc()).all()
    return render_template('expert/dashboard.html', consultations=consultations)

@expert_bp.route('/consultation/<int:consultation_id>', methods=['GET', 'POST'])
def manage_consultation(consultation_id):
    consultation = db.get_or_404(Consultation, consultation_id)
    if request.method == 'POST':
        status = request.form.get('status')
        notes = request.form.get('expert_notes', '').strip()
        allowed = {'Pending', 'Approved', 'Completed', 'Cancelled'}
        if status not in allowed:
            flash('Invalid status.', 'danger')
        else:
            consultation.status = status
            consultation.expert_notes = notes
            consultation.expert_id = current_user.id
            db.session.commit()
            flash('Consultation updated.', 'success')
            return redirect(url_for('expert.dashboard'))
    return render_template('expert/manage_consultation.html', consultation=consultation)
