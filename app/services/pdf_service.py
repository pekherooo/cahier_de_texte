import os
import base64
import pdfkit
from flask import render_template

# Configuration explicite
path_wkhtmltopdf = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)

def generate_fiche_pdf(cours, enseignant, seances, total_realise):
    logo_base64 = get_logo_base64()

    html = render_template(
        "fiche_suivi.html",
        cours=cours,
        enseignant=enseignant,
        seances=seances,
        total_realise=total_realise,
        logo_base64=logo_base64
    )

    pdf_file = pdfkit.from_string(html, False, configuration=config)
    return pdf_file

def get_logo_base64():
    logo_path = os.path.join("app", "static", "img", "logo.jpg")
    with open(logo_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode('utf-8')
