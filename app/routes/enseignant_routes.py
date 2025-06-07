from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.extensions import db
from app.models import Cours, Seance
from datetime import datetime, date, time
from app.decorators import role_required
enseignant = Blueprint('enseignant', __name__)
from sqlalchemy import func

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
    seances = Seance.query.filter_by(cours_id=cours.id).order_by(Seance.date).all()

    # Calcul du total d'heures réalisées
    total_realise = db.session.query(func.sum(Seance.duree)).filter(Seance.cours_id == cours.id).scalar() or 0

    if request.method == 'POST':
        contenu = request.form['contenu']
        duree = float(request.form['duree'])

        nouvelle_seance = Seance(
            contenu=contenu,
            duree=duree,
            cours_id=cours.id
        )

        db.session.add(nouvelle_seance)
        db.session.commit()

        flash("Séance ajoutée avec succès.", "success")
        return redirect(url_for('enseignant.cours_detail', cours_id=cours.id))

    return render_template('enseignant/cours_detail.html', cours=cours, seances=seances, total_realise=total_realise)