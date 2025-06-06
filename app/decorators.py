from functools import wraps
from flask import redirect, url_for, flash
from flask_login import current_user

def role_required(required_role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                flash("Veuillez vous connecter.", "danger")
                return redirect(url_for("auth.login"))
            if current_user.role != required_role:
                flash("Accès non autorisé.", "danger")
                return redirect(url_for("main.index"))
            return f(*args, **kwargs)
        return decorated_function
    return decorator
