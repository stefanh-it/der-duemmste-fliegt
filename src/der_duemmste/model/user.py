from flask_login import UserMixin
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean
from .. import db


class User(db.Model, UserMixin):

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(100), nullable=False)
    is_admin: Mapped[Boolean] = mapped_column(Boolean, default=False)

    def __init__(self, username: str, password: str, is_admin: bool = False):
        setattr(self, "username", username)
        setattr(self, "password", password)
        setattr(self, "is_admin", is_admin)
