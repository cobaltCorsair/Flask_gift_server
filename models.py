from sqlalchemy import Column, ForeignKey
from datetime import datetime
from app import db


# классы базы данных
class Username(db.Model):
    """Список пользователей"""
    __tablename__ = 'username'
    id = Column(db.Integer, primary_key=True)
    forum_id = Column(db.Integer(), index=True, nullable=False, unique=True)
    name = Column(db.String(120), nullable=False)
    user_send = db.relationship('user_presents', backref=db.backref('user_send', cascade="all, delete-orphan"),
                           lazy='joined')
    user_addr = db.relationship('user_presents', backref=db.backref('user_addr', cascade="all, delete-orphan"),
                           lazy='joined')

    def __repr__(self):
        return '<User %r>' % self.name


class Presents(db.Model):
    """База подарков"""
    __tablename__ = 'presents'
    id = Column(db.Integer, primary_key=True)
    name = Column(db.String(120), nullable=False)
    title = Column(db.String(500), nullable=False)
    image = Column(db.String(250), nullable=False)
    id_pres = db.relationship('user_presents', backref=db.backref('id_pres', cascade="all, delete-orphan"),
                           lazy='joined')
    name_pres = db.relationship('user_presents', backref=db.backref('name_pres', cascade="all, delete-orphan"),
                           lazy='joined')

    def __repr__(self):
        return '<Present %r>' % self.name


class UserPresents(db.Model):
    """Подарки пользователей"""
    __tablename__ = 'user_presents'
    id = Column(db.Integer(), primary_key=True)
    id_user_addressee = Column(db.Integer(), db.ForeignKey('username.id'))
    id_user_sender = Column(db.Integer(), db.ForeignKey('username.id'))
    id_present = Column(db.Integer(), db.ForeignKey('presents.id'))
    name_present = Column(db.String(120), db.ForeignKey('presents.name'))
    comment = Column(db.String(500))
    date = Column(db.DateTime(), default=datetime.utcnow)

