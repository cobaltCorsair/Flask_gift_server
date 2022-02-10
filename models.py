from sqlalchemy import Column, ForeignKey, ForeignKeyConstraint
from datetime import datetime
from app import db


# классы базы данных
class Username(db.Model):
    """Список пользователей"""
    __tablename__ = 'username'
    id = Column(db.Integer, primary_key=True)
    forum_id = Column(db.Integer(), index=True, nullable=False, unique=True)
    name = Column(db.String(120), nullable=False)
    # отношения
    user_addr = db.relationship('UserPresents', foreign_keys='UserPresents.id_user_addressee',
                                backref=db.backref('username_a', cascade="all, delete-orphan"), lazy='joined')
    user_send = db.relationship('UserPresents', foreign_keys='UserPresents.id_user_sender',
                                backref=db.backref('username_s', cascade="all, delete-orphan"), lazy='joined')

    def __repr__(self):
        return '<User %r>' % self.name


class Presents(db.Model):
    """База подарков"""
    __tablename__ = 'presents'
    id = Column(db.Integer, primary_key=True)
    name = Column(db.String(120), nullable=False)
    title = Column(db.String(500), nullable=False)
    image = Column(db.String(250), nullable=False)
    # отношения
    id_pres = db.relationship('UserPresents', foreign_keys='UserPresents.id_present',
                              backref=db.backref('presents_i', cascade="all, delete-orphan"), lazy='joined')

    def __repr__(self):
        return '<Present %r>' % self.name


class UserPresents(db.Model):
    """Подарки пользователей"""
    __tablename__ = 'user_presents'
    id = Column(db.Integer(), primary_key=True)
    id_user_addressee = Column(db.Integer(), db.ForeignKey('username.id'))
    id_user_sender = Column(db.Integer(), db.ForeignKey('username.id'))
    id_present = Column(db.Integer(), db.ForeignKey('presents.id'))
    comment = Column(db.String(500))
    date = Column(db.DateTime(), default=datetime.utcnow)

    # __table_args__ = (
    #     ForeignKeyConstraint(['id_user_addressee'], ['username.id'], name='fk_id_user_addressee'),
    #     ForeignKeyConstraint(['id_user_sender'], ['username.id'], name='fk_id_user_sender'),
    #     ForeignKeyConstraint(['id_present'], ['presents.id'], name='fk_id_present'),
    # )

