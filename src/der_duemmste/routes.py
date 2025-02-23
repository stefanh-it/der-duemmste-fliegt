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


@main_bp.route('/question_overview', methods=['GET'])
def question_overview():
    questions = Question.query.all()
    return render_template('question_overview.html', questions=questions)
