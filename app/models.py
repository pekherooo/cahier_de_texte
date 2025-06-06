
from datetime import datetime
from .extensions import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    mot_de_passe = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    cours = db.relationship('Cours', backref='enseignant', lazy=True)

class Invitation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    role = db.Column(db.String(20), nullable=False)
    token = db.Column(db.String(200), unique=True, nullable=False)
    date_expiration = db.Column(db.DateTime, nullable=False)

class Seance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    heure_debut = db.Column(db.Time, nullable=False)
    heure_fin = db.Column(db.Time, nullable=False)
    contenu = db.Column(db.Text, nullable=False)
    validee = db.Column(db.Boolean, default=False)

    cours_id = db.Column(db.Integer, db.ForeignKey('cours.id'), nullable=False)

    @property
    def duree(self):
        from datetime import datetime, date
        return datetime.combine(date.min, self.heure_fin) - datetime.combine(date.min, self.heure_debut)


class Cours(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), unique=True, nullable=False)  # Ajout du unique ici
    volume_horaire = db.Column(db.Float, nullable=False)
    coefficient = db.Column(db.Float, nullable=False)
    credits = db.Column(db.Integer, nullable=False)
    enseignant_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    seances = db.relationship('Seance', backref='cours', lazy=True)


class Validation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    responsable_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    seance_id = db.Column(db.Integer, db.ForeignKey('seance.id'), nullable=False)
    date_validation = db.Column(db.DateTime, default=datetime.utcnow)

