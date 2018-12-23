from flask import Blueprint, render_template, request, redirect, url_for, session, g, flash
from lib.models.UserModel import UserModel

top_bp = Blueprint('top', __name__, url_prefix='/')
user_model = UserModel()


@top_bp.route('/')
def index():
    return render_template('index.html')


@top_bp.route('/index')
def index2():
    return render_template('index.html')


@top_bp.route('/register', methods=['GET'])
def register_page():
    return render_template('register.html')


@top_bp.route('/register', methods=['POST'])
def register():
    user_name = request.form.get('username')
    password = request.form.get('password')
    check_password = request.form.get('password_again')

    if password != check_password:
        print('Password does not match')
        return render_template('register.html', error_message="パスワードが一致しません")
    try:
        user_model.create_user(user_name, password)
        return redirect(url_for('top.index'))
    except Exception as e:
        return render_template('register.html', error_message=str(e))

@top_bp.route('/login', methods=['POST'])
def login():
    user_name = request.form.get('username')
    password = request.form.get('password')
    user = user_model.login(user_name, password)
    if user == None:
        # Login failed
        return render_template('index.html')
    else:
        # Login success
        session['user_name'] = user.name
        session['user_id'] = user.id
        return redirect(url_for('users.user_index'))

@top_bp.route('/reset')
def render_update_password():
    return render_template('update_password.html')

@top_bp.route('/reset', methods=['POST'])
def update_password():
    user_name = request.form['username']
    new_password = request.form['password']
    new_password2 = request.form['password_again']
    if new_password == new_password2:
        user_model.update_password(user_name, new_password)
        flash('パスワードが変更されました')
        return redirect(url_for('top.index'))
    else:
        flash('パスワードが一致しません', 'error')
        return render_template('update_password.html')
