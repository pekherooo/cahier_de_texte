from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.extensions import db
from app.models import Cours, Seance
from datetime import datetime, date, time
from app.decorators import role_required
enseignant = Blueprint('enseignant', __name__)


@enseignant.route('/enseignant')
@login_required
@role_required('enseignant')
def dashboard():
    cours = Cours.query.filter_by(enseignant_id=current_user.id).all()
    return render_template('enseignant/dashboard.html', cours=cours)


@enseignant.route('/enseignant/cours/<int:cours_id>', methods=['GET', 'POST'])
@login_required
def cours_detail(cours_id):
    cours = Cours.query.get_or_404(cours_id)

    if cours.enseignant_id != current_user.id:
        flash("Accès non autorisé à ce cours.", "danger")
        return redirect(url_for('enseignant.dashboard'))

    if request.method == 'POST':
        contenu = request.form.get('contenu')
        if contenu:
            # par défaut on prend la date et l’heure de maintenant
            now = datetime.now()
            heure_debut = time(now.hour, now.minute)
            heure_fin = time(now.hour + 1, now.minute)  # simulation sur 1h
            seance = Seance(
                cours_id=cours.id,
                contenu=contenu,
                date=now.date(),
                heure_debut=heure_debut,
                heure_fin=heure_fin
            )
            db.session.add(seance)
            db.session.commit()
            flash('Séance ajoutée avec succès.', 'success')
            return redirect(url_for('enseignant.cours_detail', cours_id=cours_id))

    seances = Seance.query.filter_by(cours_id=cours.id).all()
    return render_template('enseignant/cours_detail.html', cours=cours, seances=seances)

