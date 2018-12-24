from flask import Blueprint, render_template, session, redirect, url_for, g, request
from lib.views import login_required
from lib.models.CollaborativeFiltering import CollaborativeFilter
from lib.models.UserModel import UserModel
from lib.models.Recommend import RecommendModel

user_bp = Blueprint('users', __name__, url_prefix='/user')

@login_required
@user_bp.route('/')
def user_index():
    user_model = UserModel()
    visited_places = user_model.get_all_visited_place(session['user_id'])
    return render_template('user.html', visited_place=visited_places)

@user_bp.route('/logout', methods=['GET'])
def logout():
    session.pop('user_id')
    session.pop('user_name')
    return redirect(url_for('top.index'))

@login_required
@user_bp.route('/recommend')
def recommendation():
    user_id = session.get('user_id')
    cf = CollaborativeFilter(user_id)
    recommend_matrix = cf.get_recommend(user_id)
    return render_template(url_for('user.html'))

@login_required
@user_bp.route('/review')
def render_recommend_history():
    recommend_model = RecommendModel()
    user_id = session.get('user_id')
    histories = recommend_model.get_recommend_history(user_id)
    return render_template('recommend_history.html', histories=histories)

@login_required
@user_bp.route('/review/<int:id>', methods=['GET'])
def render_review_page(id):
    recommend_model = RecommendModel()
    recommend = recommend_model.get_recommend_by_id(id)
    return render_template('review.html', recommend=recommend)

@login_required
@user_bp.route('/review/<int:id>', methods=['POST'])
def post_review(id):
    recommend_id = id
    recommend_model = RecommendModel()
    user_id = session.get('user_id')
    time_review = request.form.getlist('time_review')[0]
    distance_review = request.form.getlist('distance_review')[0]
    preference_review = request.form.getlist('preference_review')[0]
    total_review = request.form.getlist('total_review')[0]
    recommend_model.insert_review(user_id, recommend_id, total_review, time_review, preference_review, distance_review)
    return redirect(url_for('users.render_recommend_history'))




