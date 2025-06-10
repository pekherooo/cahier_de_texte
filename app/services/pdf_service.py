import os
import platform
import pdfkit
from flask import render_template
import base64

def get_wkhtmltopdf_path():
    if platform.system() == "Windows":
        return r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
    else:
        return "/usr/local/bin/wkhtmltopdf"

config = pdfkit.configuration(wkhtmltopdf=get_wkhtmltopdf_path())

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
    return pdfkit.from_string(html, False, configuration=config)

def get_logo_base64():
    logo_path = os.path.join("app", "static", "img", "logo.jpg")
    with open(logo_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode('utf-8')
