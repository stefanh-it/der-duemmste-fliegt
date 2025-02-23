from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean
from .. import db


class Question(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    question: Mapped[str] = mapped_column(String(450), nullable=False)
    answer: Mapped[str] = mapped_column(String(450), nullable=False)
    is_published: Mapped[Boolean] = mapped_column(Boolean, default=False)

    def __init__(self, question: str, answer: str, is_published: bool = False):
        setattr(self, "question", question)
        setattr(self, "answer", answer)
        setattr(self, "is_published", is_published)
