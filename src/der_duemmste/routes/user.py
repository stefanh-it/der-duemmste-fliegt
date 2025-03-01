from flask import Blueprint, render_template, request, jsonify, flash
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash
from der_duemmste.extensions import db

from der_duemmste.model.user import User

user_bp = Blueprint('user', __name__)


@user_bp.route("/register", methods=["POST"])
def register_user():
    if not request.form.get("username") or not request.form.get("password"):
        return jsonify({"error": "Username and password required"}), 400
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        try:
            new_user = User(username=username, password=generate_password_hash(password))
            db.session.add(new_user)
            db.session.commit()
            return render_template('partials/user_item.html', user=new_user)
        except IntegrityError:
            db.session.rollback()
            flash("Username already exists", "error")
            return jsonify({"error": "Username already exists"}), 400


@user_bp.route("/<int:user_id>", methods=["GET"])
def show_user(user_id: int):
    user = User.query.get_or_404(user_id)
    return render_template('partials/user_item.html', user=user)


@user_bp.route("/<int:user_id>/edit", methods=["GET"])
def edit_user(user_id: int):
    user = User.query.get_or_404(user_id)
    return render_template('partials/user_edit.html', user=user)


@user_bp.route("/<int:user_id>/update", methods=["PUT", "PATCH"])
def update_user(user_id: int):
    user = User.query.get_or_404(user_id)
    try:
        username = request.form.get("username")
        remaining_lives = request.form.get("remaining_lives")
        new_password = request.form.get("password", "").strip()

        user.username = username
        if new_password:
            user.password = generate_password_hash(new_password)

        user.remaining_lives = remaining_lives
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Username already exists"}), 400
    return render_template('partials/user_item.html', user=user)


@user_bp.route("/<int:user_id>/delete", methods=["DELETE"])
def delete_user(user_id: int):
    user = User.query.get(user_id)
    if not user:
        return {"error": "User not found"}, 404
    db.session.delete(user)
    db.session.commit()
    return '', 200
