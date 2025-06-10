from flask import Blueprint, render_template, request, redirect, url_for, flash, send_file
from flask_login import login_required
from app.models import Invitation, User, Cours, Seance
from app.extensions import db
from app.services.email_service import send_email
from app.decorators import role_required
from app.services.invitation_service import create_or_update_invitation
from app.services.pdf_service import generate_fiche_pdf
from flask import send_file
from io import BytesIO
from sqlalchemy import func
from app.services.graphiques import graphe_progression_par_cours, graphe_cumul_heures_par_semaine



chef = Blueprint('chef', __name__)

@chef.route('/chef/inviter_utilisateur', methods=['GET', 'POST'])
@login_required
def inviter_utilisateur():
    if request.method == 'POST':
        nom = request.form['nom']
        email = request.form['email']
        role = request.form['role']

        invitation = create_or_update_invitation(nom, email, role)

        lien = url_for('auth.complete_registration', token=invitation.token, _external=True)
        subject = "Inscription à l'application Cahier de Texte"
        body = f"Bonjour {nom},\n\nVous avez été invité à rejoindre l'application.\n\nLien valable 24h :\n{lien}"

        send_email(subject, [email], body)

        flash('Invitation envoyée ou mise à jour avec succès.', 'success')
        return redirect(url_for('chef.dashboard'))

    return render_template('chef/inviter_utilisateur.html')

@chef.route('/chef/utilisateurs')
@login_required
def liste_utilisateurs():
    utilisateurs = User.query.filter(User.role != 'chef').all()
    return render_template('chef/liste_utilisateurs.html', utilisateurs=utilisateurs)

@chef.route('/chef/supprimer_utilisateur/<int:user_id>', methods=['POST'])
@login_required
def supprimer_utilisateur(user_id):
    utilisateur = User.query.get_or_404(user_id)
    if utilisateur.role == 'chef':
        flash("Impossible de supprimer un chef de filière.", "danger")
        return redirect(url_for('chef.liste_utilisateurs'))
    db.session.delete(utilisateur)
    db.session.commit()
    flash("Utilisateur supprimé avec succès.", "success")
    return redirect(url_for('chef.liste_utilisateurs'))


@chef.route('/chef/suivi_enseignant', methods=['GET', 'POST'])
@login_required
def suivi_enseignant():
    enseignants = User.query.filter_by(role='enseignant').all()
    enseignant_id = request.form.get('enseignant_id') if request.method == 'POST' else None
    cours_id = request.form.get('cours_id') if request.method == 'POST' else None

    cours = []
    seances = []

    if enseignant_id:
        cours = Cours.query.filter_by(enseignant_id=enseignant_id).all()
        if cours_id:
            cours_selected = Cours.query.get(int(cours_id))
            seances = Seance.query.filter_by(cours_id=cours_selected.id).order_by(Seance.date).all()
        else:
            cours_selected = None
    else:
        cours_selected = None

    return render_template('chef/suivi_enseignant.html',
                           enseignants=enseignants,
                           cours=cours,
                           enseignant_id=enseignant_id,
                           cours_selected=cours_selected,
                           seances=seances)


@chef.route('/chef/invitations')
@login_required
def liste_invitations():
    invitations = Invitation.query.order_by(Invitation.date_expiration.desc()).all()
    return render_template('chef/liste_invitations.html', invitations=invitations)

@chef.route('/chef/supprimer_invitation/<int:invitation_id>', methods=['POST'])
@login_required
def supprimer_invitation(invitation_id):
    invitation = Invitation.query.get_or_404(invitation_id)
    db.session.delete(invitation)
    db.session.commit()
    flash("Invitation supprimée avec succès.", "success")
    return redirect(url_for('chef.liste_invitations'))


@chef.route('/chef/creer_cours', methods=['GET', 'POST'])
@login_required
def creer_cours():
    enseignants = User.query.filter_by(role='enseignant').all()

    if request.method == 'POST':
        nom = request.form['nom']
        volume_horaire = int(request.form['volume_horaire'])
        coefficient = int(request.form['coefficient'])
        credits = int(request.form['credits'])
        enseignant_id = request.form.get('enseignant_id')

        # Vérification des bornes
        if coefficient < 1 or coefficient > 10:
            flash("Le coefficient doit être compris entre 1 et 10.", "danger")
            return redirect(url_for('chef.creer_cours'))

        if volume_horaire < 2 or volume_horaire > 50 or volume_horaire % 2 != 0:
            flash("Le Volume Horaire Total doit être un nombre pair entre 2 et 50.", "danger")
            return redirect(url_for('chef.creer_cours'))

        # Vérification unicité du nom de cours
        existing_cours = Cours.query.filter_by(nom=nom).first()
        if existing_cours:
            flash("Un cours avec ce nom existe déjà.", "danger")
            return redirect(url_for('chef.creer_cours'))

        # Création du cours
        nouveau_cours = Cours(
            nom=nom,
            volume_horaire=volume_horaire,
            coefficient=coefficient,
            credits=credits,
            enseignant_id=enseignant_id
        )

        db.session.add(nouveau_cours)
        db.session.commit()

        flash("Cours créé et assigné avec succès.", "success")
        return redirect(url_for('chef.dashboard'))

    return render_template('chef/creer_cours.html', enseignants=enseignants)




@chef.route('/chef/fiche_suivi_pdf/<int:cours_id>')
@login_required
def fiche_suivi_pdf(cours_id):
    cours = Cours.query.get_or_404(cours_id)
    enseignant = cours.enseignant
    seances = Seance.query.filter_by(cours_id=cours.id).order_by(Seance.date).all()

    total_realise = db.session.query(func.sum(Seance.duree)).filter(Seance.cours_id == cours.id).scalar() or 0

    pdf_bytes = generate_fiche_pdf(cours, enseignant, seances, total_realise)

    return send_file(
        BytesIO(pdf_bytes),
        as_attachment=True,
        download_name=f"fiche_suivi_{cours.nom}_{enseignant.nom}.pdf",
        mimetype="application/pdf"
    )

@chef.route('/chef/visualisation/<int:cours_id>')
@login_required
def visualisation_cours(cours_id):
    cours = Cours.query.get_or_404(cours_id)
    seances = Seance.query.filter_by(cours_id=cours.id).order_by(Seance.date).all()

    img1_base64 = graphe_progression_par_cours(cours, seances)
    img2_base64 = graphe_cumul_heures_par_semaine(seances)

    return render_template('chef/visualisation.html', cours=cours, img1_base64=img1_base64, img2_base64=img2_base64)

@chef.route('/chef/dashboard')
@login_required
@role_required('chef')
def dashboard():
    return render_template('chef/dashboard.html')
