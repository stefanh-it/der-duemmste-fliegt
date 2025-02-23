import sys
from getpass import getpass
from werkzeug.security import generate_password_hash
from sqlalchemy.exc import IntegrityError
from src.der_duemmste import create_app, db
from src.der_duemmste.model.user import User

app = create_app()


def create_admin():
    with app.app_context():
        username = input("Enter admin username: ")
        password = getpass("Enter admin password: ")
        password_confirm = getpass("Confirm admin password: ")
        if password != password_confirm:
            sys.exit("Passwords do not match")
        user = User.query.filter_by(username=username).first()
        if user:
            sys.exit("Admin already exists")
        try:
            new_user = User(
                username=username,
                password=generate_password_hash(password),
                is_admin=True
            )
            db.session.add(new_user)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            sys.exit("Admin already exists")
        print("Admin created")


if __name__ == "__main__":
    create_admin()
