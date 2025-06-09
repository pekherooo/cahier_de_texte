import os
from flask import render_template
from weasyprint import HTML
from app.models import Cours, Seance, User
from app.extensions import db
from sqlalchemy import func
import base64


def generer_fiche_suivi_pdf(cours_id):
    cours = Cours.query.get(cours_id)
    enseignant = User.query.get(cours.enseignant_id)
    seances = Seance.query.filter_by(cours_id=cours_id).order_by(Seance.date).all()
    total_realise = db.session.query(func.sum(Seance.duree)).filter(Seance.cours_id == cours_id).scalar() or 0

    html = render_template("fiche_suivi.html", cours=cours, enseignant=enseignant, seances=seances, total_realise=total_realise)

    logo_base64 = get_logo_base64()

    html = render_template(
        "fiche_suivi.html",
        cours=cours,
        enseignant=enseignant,
        seances=seances,
        total_realise=total_realise,
        logo_base64=logo_base64
    )

    output_path = os.path.join(os.getcwd(), f"FICHE_SUIVI_{cours.nom}_{enseignant.nom}.pdf")
    HTML(string=html).write_pdf(output_path)

    return output_path



def get_logo_base64():
    logo_path = os.path.join(os.getcwd(), "static", "img", "logo.jpg")
    with open(logo_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode('utf-8')
