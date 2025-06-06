from datetime import datetime, timedelta
from app.models import Invitation
from app.extensions import db
import secrets

from datetime import datetime, timedelta
from app.models import Invitation
from app.extensions import db
import secrets

def create_or_update_invitation(nom, email, role, valid_hours=48):
    token = secrets.token_urlsafe(32)
    expiration = datetime.utcnow() + timedelta(hours=valid_hours)

    invitation = Invitation.query.filter_by(email=email).first()

    if invitation:
        # Met à jour le token et la date d'expiration
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
    return invitation


def purge_expired_invitations():
    expired = Invitation.query.filter(Invitation.date_expiration < datetime.utcnow()).all()
    for inv in expired:
        db.session.delete(inv)
    db.session.commit()

