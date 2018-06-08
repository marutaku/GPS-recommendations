from flask import Blueprint, render_template, request, redirect, url_for
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
    if user_model.create_user(user_name, password) == False:
        print('user name is duplicate')
        return render_template('register.html', error_message="ユーザー名が重複しています")
    return redirect(url_for('top.index'))

@top_bp.route('/login', methods=['POST'])
def login():
    user_name = request.form.get('username')
    password = request.form.get('password')
    if user_model.login(user_name, password):
        return redirect(url_for('users.user_index'))
    else:
        return render_template('index.html')
