from flask import Blueprint, render_template
from lib.views import login_required

user_bp = Blueprint('users', __name__, url_prefix='/user')

@login_required
@user_bp.route('/')
def user_index():
    return render_template('user.html')

@login_required
@user_bp.route('/int:<id>')
def user_page(id):
    return render_template('user.html')




