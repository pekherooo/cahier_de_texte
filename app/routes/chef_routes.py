from flask import Blueprint, render_template, request, redirect, url_for, flash, send_file
from flask_login import login_required
from app.models import Invitation, User, Cours, Seance
from app.extensions import db
from app.services.email_service import send_email
from app.decorators import role_required
from app.services.invitation_service import create_or_update_invitation


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

    cours = []
    if enseignant_id:
        cours = Cours.query.filter_by(enseignant_id=enseignant_id).all()

    return render_template(
        'chef/suivi_enseignant.html',
        enseignants=enseignants,
        cours=cours,
        enseignant_id=enseignant_id
    )

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


@chef.route('/chef/dashboard')
@login_required
@role_required('chef')
def dashboard():
    return render_template('chef/dashboard.html')
