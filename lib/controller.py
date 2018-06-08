from flask import render_template, json, session, request, redirect, url_for, g
from functools import wraps
from lib.database.User import User
from lib import app
from lib.models.UserModel import UserModel

# TODO Separate function to /views

user_model = UserModel()


def login_required(f):
    @wraps(f)
    def decorated_view(*args, **kwargs):
        if g.user is None:
            return redirect(url_for('index', next=request.path))
        return f(*args, **kwargs)

    return decorated_view


@app.before_request
def load_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get(session['user_id'])


@app.route('/login', methods=['POST'])
def login():
    username = request.form('username')
    password = request.form('password')
    login_user = user_model.login(username, password)
    if (login_user):
        session['user_id'] =login_user.id
        redirect(url_for('home.html'))
    else:
        redirect(url_for('index.html'))
#
# @app.route('/index')
# def index():
#     return render_template('index.html')
#
#
# @app.route('/')
# def index2():
#     return render_template('index.html')


@login_required
@app.route('/home')
def home():
    username = session.get('username')
    render_template('home.html', name=username)


@app.route('/detail')
def detail():
    return render_template('detail.html')

