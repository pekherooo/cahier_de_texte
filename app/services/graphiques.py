import matplotlib.pyplot as plt
import base64
from io import BytesIO
from datetime import datetime
from collections import defaultdict

def convertir_graphique_en_base64(fig):
    buffer = BytesIO()
    fig.savefig(buffer, format='png', bbox_inches='tight')
    buffer.seek(0)
    return base64.b64encode(buffer.getvalue()).decode('utf-8')

def graphe_progression_par_cours(cours, seances):
    realise = sum([s.duree.total_seconds() for s in seances]) / 3600
    prevu = cours.volume_horaire

    fig, ax = plt.subplots()
    ax.bar(['Prévu', 'Réalisé'], [prevu, realise], color=['gray', 'blue'])
    ax.set_ylabel('Heures')
    ax.set_title(f'Progression du cours : {cours.nom}')
    return convertir_graphique_en_base64(fig)

def graphe_cumul_heures_par_semaine(seances):
    cumul_hebdo = defaultdict(float)
    for s in seances:
        semaine = s.date.isocalendar()[1]
        cumul_hebdo[semaine] += s.duree.total_seconds() / 3600

    semaines = sorted(cumul_hebdo.keys())
    heures = [sum([cumul_hebdo[w] for w in semaines[:i+1]]) for i in range(len(semaines))]

    fig, ax = plt.subplots()
    ax.plot(semaines, heures, marker='o', color='green')
    ax.set_xlabel('Semaine')
    ax.set_ylabel('Cumul des heures')
    ax.set_title('Évolution hebdomadaire des heures')
    ax.grid(True)
    return convertir_graphique_en_base64(fig)
