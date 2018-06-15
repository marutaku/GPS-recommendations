from flask import Blueprint, render_template, session, redirect, url_for, g
from lib.views import login_required

user_bp = Blueprint('users', __name__, url_prefix='/user')

@login_required
@user_bp.route('/')
def user_index():
    print(g.user)
    return render_template('user.html')

@login_required
@user_bp.route('/int:<id>')
def user_page(id):
    return render_template('user.html')

@user_bp.route('/logout', methods=['GET'])
def logout():
    session.pop('user_id')
    return redirect(url_for('top.index'))




