from app import create_app
from app.extensions import db

# Crée une app Flask via ton factory existante
app = create_app()

with app.app_context():
    print("⚠ Attention : cette opération va supprimer toutes les données existantes de la base...")

    # Drop toutes les tables existantes
    db.drop_all()
    print("✅ Toutes les tables supprimées.")

    # Recrée toutes les tables à partir de tes modèles
    db.create_all()
    print("✅ Les tables ont été recréées (base propre et vide).")

    print("🎯 Base de données réinitialisée avec succès.")
