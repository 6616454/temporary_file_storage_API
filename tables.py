import sqlalchemy as sa

from sqlalchemy.orm import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = sa.Column(sa.Integer, primary_key=True)
    username = sa.Column(sa.String(32), unique=True, nullable=False)
    email = sa.Column(sa.String(100), unique=True, nullable=True)
    password_hash = sa.Column(sa.Text)
    user_path = sa.Column(sa.Text, unique=True, nullable=False)


class File(Base):
    __tablename__ = 'files'
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(64), nullable=False)
    file = sa.Column(sa.Text, nullable=False)
    link = sa.Column(sa.Text, nullable=True)
    public = sa.Column(sa.Boolean, default=False)
    user_id = sa.Column(sa.Integer, sa.ForeignKey('users.id'), nullable=False)
