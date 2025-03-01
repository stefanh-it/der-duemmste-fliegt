from werkzeug.security import generate_password_hash
from src.der_duemmste import create_app
from src.der_duemmste.extensions import db
from src.der_duemmste.model.question import Question
from src.der_duemmste.model.user import User


app = create_app()

with app.app_context():
    db.create_all()

    if not db.session.query(User).first():
        user = User(
            username="admin",
            password="admin",
            is_admin=True
        )
        db.session.add(user)
        db.session.commit()
        print("User created.")

    if db.session.query(Question).first():
        db.session.query(Question).delete()

    sample_questions = [
        Question("What is the capital of Germany?", "Berlin"),
        Question("What is the capital of France?", "Paris"),
        Question("What is the capital of Italy?", "Rome"),
        Question("What is the capital of Spain?", "Madrid"),
        Question("What is the capital of Portugal?", "Lisbon"),
        Question("What is the capital of the United Kingdom?", "London"),
        Question("What is the capital of the United States?", "Washington, D.C."),
        Question("What is the capital of Canada?", "Ottawa"),
        Question("What is the capital of Mexico?", "Mexico City"),
        Question("What is the capital of Brazil?", "Brasília"),
        Question("What is the capital of Argentina?", "Buenos Aires"),
        Question("What is the capital of Australia?", "Canberra"),
        Question("What is the capital of Japan?", "Tokyo"),
        Question("What is the capital of China?", "Beijing"),
        Question("What is the capital of India?", "New Delhi"),
        Question("What is the capital of Russia?", "Moscow"),
        Question("What is the capital of South Africa?", "Pretoria"),
        Question("What is the capital of Nigeria?", "Abuja"),
        Question("What is the capital of Egypt?", "Cairo"),
        Question("What is the capital of Saudi Arabia?", "Riyadh"),
        Question("What is the capital of Turkey?", "Ankara"),
        Question("What is the capital of Iran?", "Tehran"),
        Question("What is the capital of Iraq?", "Baghdad"),
        Question("What is the capital of Afghanistan?", "Kabul"),
        Question("What is the capital of Pakistan?", "Islamabad"),
        Question("What is the capital of Switzerland?", "Bern"),
        Question("What is the capital of Somalia", "Mogadishu"),
        Question("What is the capital of Sweden?", "Stockholm"),
        Question("What is the capital of South Korea?", "Seoul"),
        Question("What is the capital of North Korea?", "Pyongyang"),
        Question("What is the capital of Thailand?", "Bangkok"),
        Question("What is the capital of Vietnam?", "Hanoi"),
        Question("What is the capital of Malaysia?", "Kuala Lumpur"),
    ]
    db.session.add_all(sample_questions)
    print("Questions created")

    sample_players = [
        User("player1", generate_password_hash("player1"), False),
        User("player2", generate_password_hash("player2"), False),
        User("player3", generate_password_hash("player3"), False),
        User("player4", generate_password_hash("player4"), False),
        User("player5", generate_password_hash("player5"), False),
    ]

    db.session.query(User).filter_by(is_admin=False).delete()
    db.session.add_all(sample_players)
    print("Players created")

    db.session.commit()
    print("Database seeded.")
