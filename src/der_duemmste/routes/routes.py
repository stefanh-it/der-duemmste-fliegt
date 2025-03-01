from flask import Blueprint, render_template, request

from der_duemmste.model.question import Question
from der_duemmste.model.user import User

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    return render_template('index.html')


@main_bp.route('/test')
def test():
    return render_template('base.html')


@main_bp.route('/player_overview', methods=['GET'])
def list_players():
    page = request.args.get('page', 1, type=int)
    per_page = 20
    pagination = User.query.order_by(User.id.desc()).filter_by(is_admin=False).paginate(
        page=page, per_page=per_page, error_out=False
    )
    context = {
        'users': pagination.items,
        'pagination': pagination,
        'endpoint': 'main.list_players',
        'target': '#users-container'}
    if request.headers.get('HX-Request'):
        return render_template(
            'partials/user_list.html', **context
        )
    return render_template('player_overview.html', **context)


@main_bp.route('/question_overview', methods=['GET'])
def list_questions():
    page = request.args.get('page', 1, type=int)
    per_page = 20
    pagination = Question.query.order_by(Question.id.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    context = {
        'questions': pagination.items,
        'pagination': pagination,
        'endpoint': 'main.list_questions',
        'target': '#questions-container'}

    if request.headers.get('HX-Request'):
        return render_template(
            'partials/question_list.html', **context
        )

    return render_template('question_overview.html', **context)

