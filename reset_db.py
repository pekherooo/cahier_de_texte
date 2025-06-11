from app import create_app, db
from app.models import User
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    # Réinitialiser la base
    print("Suppression des tables...")
    db.drop_all()

    print("Création des tables...")
    db.create_all()

    # Créer un compte admin par défaut
    print("Création de l'utilisateur admin...")
    admin = User(
        nom="admin",
        email="admin@univ-thies.sn",
        mot_de_passe=generate_password_hash("admin123"),
        role="chef"  # ou "admin" si tu as ce rôle
    )
    db.session.add(admin)
    db.session.commit()

    print("✔️ Réinitialisation terminée. Admin : admin@univ-thies.sn / admin123")
