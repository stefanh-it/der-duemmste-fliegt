from flask import Blueprint, render_template, request, jsonify
from sqlalchemy.exc import IntegrityError

from der_duemmste.extensions import db

# from der_duemmste.model.question import Question
# from der_duemmste.model.user import User

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    return render_template('index.html')


@main_bp.route('/test')
def test():
    return render_template('base.html')


@main_bp.route('/player_overview', methods=['GET'])
def list_players():
    from der_duemmste.model.user import User
    page = request.args.get('page', 1, type=int)
    per_page = 20
    pagination = User.query.order_by(User.id.desc()).filter_by(is_admin=False).paginate(
        page=page, per_page=per_page, error_out=False
    )
    if request.headers.get('HX-Request'):
        return render_template(
            'partials/user_list.html',
            users=pagination.items,
            pagination=pagination
        )
    return render_template('player_overview.html')


@main_bp.route('/question_overview', methods=['GET'])
def list_questions():
    from der_duemmste.model.question import Question
    page = request.args.get('page', 1, type=int)
    per_page = 20
    pagination = Question.query.order_by(Question.id.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )

    if request.headers.get('HX-Request'):
        return render_template(
            'partials/question_list.html',
            questions=pagination.items,
            pagination=pagination
        )

    return render_template('question_overview.html',
                           questions=pagination.items,
                           pagination=pagination)


# Create a new question
@main_bp.route('/questions', methods=['POST'])
def create_question():
    from der_duemmste.model.question import Question
    question_text = request.form['question']
    question_answer = request.form['answer']

    if not question_text or not question_answer:
        return jsonify({'error': 'Invalid question form input'}), 400

    try:
        new_question = Question(question_text, question_answer)
        db.session.add(new_question)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Question already exists'}), 400

    return render_template('partials/question_item.html', question=new_question)

# Retrieve a question


@main_bp.route('/questions/<int:question_id>', methods=['GET'])
def show_question(question_id):
    from der_duemmste.model.question import Question
    question = Question.query.get_or_404(question_id)
    return render_template('partials/question_item.html', question=question)


@main_bp.route('/questions/<int:question_id>/edit', methods=['GET'])
def edit_question(question_id):
    from der_duemmste.model.question import Question
    question = Question.query.get_or_404(question_id)
    return render_template('partials/question_edit.html', question=question)


@main_bp.route('/update_question/<int:question_id>', methods=['PUT', 'PATCH'])
def update_question(question_id):
    from der_duemmste.model.question import Question
    question = Question.query.get_or_404(question_id)
    question_text = request.form['question']
    question_answer = request.form['answer']
    if not question_text or not question_answer:
        return jsonify({'error': 'Invalid question form input'}), 400

    question.question = question_text
    question.answer = question_answer
    db.session.commit()
    return render_template('partials/question_item.html', question=question)


@main_bp.route('/questions/<int:question_id>/delete', methods=['DELETE'])
def delete_question(question_id):
    from der_duemmste.model.question import Question
    question = Question.query.get(question_id)
    if not question:
        return jsonify({'error': 'Question not found'}), 404
    db.session.delete(question)
    db.session.commit()
    return '', 200
