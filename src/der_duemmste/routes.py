from flask import Blueprint, render_template, request, jsonify
from sqlalchemy.exc import IntegrityError
from .model.question import Question
from . import db

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    return render_template('index.html')


@main_bp.route('/test')
def test():
    return render_template('base.html')


@main_bp.route('/question_overview', methods=['GET'])
def list_questions():
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


@main_bp.route('/add_question', methods=['POST'])
def add_question():
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


@main_bp.route('/delete_question/<int:question_id>', methods=['DELETE'])
def delete_question(question_id):
    question = Question.query.get(question_id)
    if not question:
        return jsonify({'error': 'Question not found'}), 404
    db.session.delete(question)
    db.session.commit()
    return '', 200
