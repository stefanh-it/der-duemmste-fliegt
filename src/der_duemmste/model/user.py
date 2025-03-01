from flask_login import UserMixin
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean
from der_duemmste.extensions import db


class User(db.Model, UserMixin):

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(100), nullable=False)
    is_admin: Mapped[Boolean] = mapped_column(Boolean, default=False)
    remaining_lives: Mapped[int] = mapped_column(Integer, default=2)

    def __init__(
            self,
            username: str,
            password: str,
            is_admin: bool = False,
            remaining_lives: int = 2
    ):
        setattr(self, "username", username)
        setattr(self, "password", password)
        setattr(self, "is_admin", is_admin)
        setattr(self, "remaining_lives", 2)
