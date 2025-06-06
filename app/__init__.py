from flask import Flask
from .extensions import db, login_manager, mail
from flask_migrate import Migrate

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)  # <--- C'est ça qu'il faut absolument avoir !
    migrate = Migrate(app, db)

    from .routes.auth_routes import auth
    from .routes.routes import main
    from .routes.enseignant_routes import enseignant
    from .routes.responsable_routes import responsable
    from .routes.chef_routes import chef

    app.register_blueprint(auth)
    app.register_blueprint(main)
    app.register_blueprint(enseignant)
    app.register_blueprint(responsable)
    app.register_blueprint(chef)

    return app
