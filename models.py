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
    user_addr = db.relationship('UserPresents', backref='username_a', cascade="all,delete",
                                foreign_keys='UserPresents.id_user_addressee')
    user_send = db.relationship('UserPresents', backref='username_s',
                                foreign_keys='UserPresents.id_user_sender')

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
    id_pres = db.relationship('UserPresents', backref='presents_i',
                              cascade="all,delete", foreign_keys='UserPresents.id_present')

    def __repr__(self):
        return '<Present %r>' % self.name


class UserPresents(db.Model):
    """Подарки пользователей"""
    __tablename__ = 'user_presents'
    id = Column(db.Integer(), primary_key=True)
    id_user_addressee = Column(db.Integer(), db.ForeignKey(Username.id))
    id_user_sender = Column(db.Integer(), db.ForeignKey(Username.id))
    id_present = Column(db.Integer(), db.ForeignKey(Presents.id))
    comment = Column(db.String(500))
    date = Column(db.DateTime(), default=datetime.utcnow)

    def serialize(self):
        """Метод для сериализации объекта"""
        return {
                "id": self.id,
                "id_user_addressee": self.id_user_addressee,
                "id_user_sender": self.id_user_sender,
                "id_present": self.id_present,
                "comment": self.comment,
                "date": self.date
                }
