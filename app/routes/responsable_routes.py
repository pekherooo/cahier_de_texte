from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required
from app.extensions import db
from app.models import Seance
from app.decorators import role_required
responsable = Blueprint('responsable', __name__)

@responsable.route('/responsable')
@login_required
@role_required('responsable')
def dashboard():
    seances = Seance.query.all()
    return render_template('responsable/dashboard.html', seances=seances)

@responsable.route('/responsable/valider/<int:seance_id>')
@login_required
def valider_seance(seance_id):
    seance = Seance.query.get_or_404(seance_id)
    if not seance.validee:
        seance.validee = True
        db.session.commit()
        flash("Séance validée avec succès.", "success")
    else:
        flash("La séance était déjà validée.", "info")
    return redirect(url_for('responsable.dashboard'))

