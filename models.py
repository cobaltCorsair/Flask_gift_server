# для настройки баз данных
from sqlalchemy import Column, ForeignKey
from datetime import datetime
from app import db


# здесь добавим классы
class Username(db.Model):
    __tablename__ = 'username'
    id = Column(db.Integer, primary_key=True)
    forum_id = Column(db.Integer(), index=True, nullable=False, unique=True)
    name = Column(db.String(120), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.name


class Presents(db.Model):
    __tablename__ = 'presents'
    id = Column(db.Integer, primary_key=True)
    name = Column(db.String(120), nullable=False)
    title = Column(db.String(500), nullable=False)
    image = Column(db.String(250), nullable=False)

    def __repr__(self):
        return '<Present %r>' % self.name


class UserPresents(db.Model):
    __tablename__ = 'user_presents'
    id = Column(db.Integer(), primary_key=True)
    id_user_addressee = Column(db.Integer(), ForeignKey('username.id'))
    id_user_sender = Column(db.Integer(), ForeignKey('username.id'))
    id_present = Column(db.Integer(), ForeignKey('presents.id'))
    name_present = Column(db.String(120), ForeignKey('presents.name'))
    comment = Column(db.String(500))
    date = Column(db.DateTime(), default=datetime.utcnow)

    user = db.relationship('Username',
                           backref=db.backref('presents', cascade="all, delete-orphan"),
                           lazy='joined')
