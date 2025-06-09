from datetime import datetime, timedelta
from app.models import Invitation
from app.extensions import db
from app.services.email_service import send_email
import secrets

# URL de ton application Render
SERVER_URL = "https://cahier-de-texte-1.onrender.com"

def create_or_update_invitation(nom, email, role, valid_hours=48):
    token = secrets.token_urlsafe(32)
    expiration = datetime.utcnow() + timedelta(hours=valid_hours)

    invitation = Invitation.query.filter_by(email=email).first()

    if invitation:
        # Mise à jour de l'invitation existante
        invitation.token = token
        invitation.date_expiration = expiration
        invitation.nom = nom
        invitation.role = role
    else:
        invitation = Invitation(
            nom=nom,
            email=email,
            role=role,
            token=token,
            date_expiration=expiration
        )
        db.session.add(invitation)

    db.session.commit()

    # Génération du lien d'inscription
    lien_inscription = f"{SERVER_URL}/complete_registration/{token}"

    # Préparer le contenu de l'e-mail
    subject = "Invitation à rejoindre la plateforme pédagogique - Université Iba Der Thiam de Thiès"

    body = f"""
Bonjour {nom},

Vous avez été invité à rejoindre la plateforme numérique de gestion pédagogique de l’Université Iba Der Thiam de Thiès.

Grâce à cette plateforme, vous pourrez notamment :

- Accéder à vos espaces personnels et vos tableaux de bord pédagogiques
- Gérer les cours, les séances, les affectations et les validations
- Suivre l’évolution des volumes horaires et des activités pédagogiques
- Générer et consulter les fiches de suivi pédagogiques
- Assurer un suivi rigoureux, centralisé et sécurisé de l’ensemble des enseignements

Veuillez finaliser votre inscription en cliquant sur le lien suivant :

👉 {lien_inscription}

Une fois inscrit, vous pourrez accéder à la plateforme via le lien :

👉 {SERVER_URL}

Cordialement,

Service Pédagogique — Département Génie Civil
Université Iba Der Thiam de Thiès
"""

    send_email(subject, [email], body)

    return invitation

def purge_expired_invitations():
    expired = Invitation.query.filter(Invitation.date_expiration < datetime.utcnow()).all()
    for inv in expired:
        db.session.delete(inv)
    db.session.commit()
