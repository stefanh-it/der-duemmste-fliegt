
from flask import Blueprint, render_template, request, jsonify
from sqlalchemy.exc import IntegrityError
from der_duemmste.extensions import db

from der_duemmste.model.question import Question

questions_bp = Blueprint('questions', __name__)


@questions_bp.route('/', methods=['POST'])
def create_question():

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


@questions_bp.route('/<int:question_id>', methods=['GET'])
def show_question(question_id):
    question = Question.query.get_or_404(question_id)
    return render_template('partials/question_item.html', question=question)


@questions_bp.route('/<int:question_id>/edit', methods=['GET'])
def edit_question(question_id):
    question = Question.query.get_or_404(question_id)
    return render_template('partials/question_edit.html', question=question)


@questions_bp.route('/<int:question_id>/update', methods=['PUT', 'PATCH'])
def update_question(question_id):
    question = Question.query.get_or_404(question_id)
    question_text = request.form['question']
    question_answer = request.form['answer']
    if not question_text or not question_answer:
        return jsonify({'error': 'Invalid question form input'}), 400

    question.question = question_text
    question.answer = question_answer
    db.session.commit()
    return render_template('partials/question_item.html', question=question)


@questions_bp.route('/<int:question_id>/delete', methods=['DELETE'])
def delete_question(question_id):
    question = Question.query.get(question_id)
    if not question:
        return jsonify({'error': 'Question not found'}), 404
    db.session.delete(question)
    db.session.commit()
    return '', 200
