
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, Length, EqualTo

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    mot_de_passe = PasswordField('Mot de passe', validators=[DataRequired()])
    submit = SubmitField('Se connecter')

class RegisterForm(FlaskForm):
    nom = StringField('Nom complet', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    mot_de_passe = PasswordField('Mot de passe', validators=[DataRequired(), Length(min=6)])
    confirm = PasswordField('Confirmer le mot de passe', validators=[DataRequired(), EqualTo('mot_de_passe')])
    role = SelectField('Rôle', choices=[('enseignant', 'Enseignant'), ('responsable', 'Responsable'), ('chef', 'Chef de filière')])
    submit = SubmitField('Créer un compte')
