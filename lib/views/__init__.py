from functools import wraps
from flask import current_app, request, redirect, url_for, \
        session, g, send_from_directory
from lib.database.User import User

def login_required(f):
    @wraps(f)
    def decorated_view(*args, **kwargs):
        if g.user is None:
            return redirect(url_for('index', next=request.path))
        return f(*args, **kwargs)

    return decorated_view

def load_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get(session['user_id'])


def init_app(app):
    # Set before_request
    app.before_request(load_user)
    # Register Blueprint
    from lib.views.TopView import top_bp
    from lib.views.UserViews import user_bp
    app.register_blueprint(user_bp)
    app.register_blueprint(top_bp)
