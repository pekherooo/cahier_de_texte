from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db, login_manager
from app.forms import LoginForm, RegisterForm
from app.models import User, Invitation
from app.services.email_service import send_email
from werkzeug.exceptions import BadRequest
from datetime import datetime

auth = Blueprint('auth', __name__)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user and check_password_hash(user.mot_de_passe, form.mot_de_passe.data):
            login_user(user)
            flash('Connexion réussie', 'success')

            # Table de redirection centralisée
            ROLES_REDIRECT = {
                'enseignant': 'enseignant.dashboard',
                'responsable': 'responsable.dashboard',
                'chef': 'chef.dashboard'
            }

            # Redirection selon le rôle (ou accueil par défaut)
            return redirect(url_for(ROLES_REDIRECT.get(user.role, 'main.index')))

        flash('Email ou mot de passe invalide.', 'danger')

    return render_template('login.html', form=form)



@auth.route('/complete_registration/<token>', methods=['GET', 'POST'])
def complete_registration(token):
    invitation = Invitation.query.filter_by(token=token).first()

    if not invitation:
        flash("Lien d'invitation invalide ou déjà utilisé.", "danger")
        return redirect(url_for('auth.login'))

    if invitation.date_expiration < datetime.utcnow():
        db.session.delete(invitation)
        db.session.commit()
        flash("Ce lien d’invitation a expiré.", "warning")
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        password = request.form['password']

        if not password or len(password) < 6:
            flash("Le mot de passe doit contenir au moins 6 caractères.", "danger")
            return render_template('complete_registration.html', invitation=invitation)

        hashed = generate_password_hash(password)
        user = User(
            nom=invitation.nom,
            email=invitation.email,
            mot_de_passe=hashed,
            role=invitation.role
        )
        db.session.add(user)
        db.session.delete(invitation)  # Supprime définitivement l’invitation après usage
        db.session.commit()

        flash("Inscription complétée avec succès. Vous pouvez maintenant vous connecter.", "success")
        return redirect(url_for('auth.login'))

    return render_template('complete_registration.html', invitation=invitation)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Déconnecté avec succès.', 'info')
    return redirect(url_for('auth.login'))
