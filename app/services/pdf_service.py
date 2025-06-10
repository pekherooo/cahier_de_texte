from flask import render_template
from xhtml2pdf import pisa
from io import BytesIO
import base64
import os

def generate_fiche_pdf(cours, enseignant, seances, total_realise):
    # ✅ Chemin correct vers le logo
    logo_path = os.path.join("app", "static", "img", "logo.jpg")

    # Encodage en base64
    with open(logo_path, "rb") as image_file:
        logo_base64 = base64.b64encode(image_file.read()).decode("utf-8")

    # Rendu HTML avec le template fiche_suivi.html
    html = render_template(
        "fiche_suivi.html",
        cours=cours,
        enseignant=enseignant,
        seances=seances,
        total_realise=total_realise,
        logo_base64=logo_base64
    )

    # Conversion en PDF
    result = BytesIO()
    pisa_status = pisa.CreatePDF(src=html, dest=result, encoding='utf-8')

    if pisa_status.err:
        raise Exception("Erreur lors de la génération du PDF")

    return result.getvalue()
