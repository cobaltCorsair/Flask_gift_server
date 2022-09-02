from sqlalchemy import Column, ForeignKey, ForeignKeyConstraint
from datetime import datetime
from app import db


# классы базы данных
class Username(db.Model):
    """Список пользователей"""
    __tablename__ = 'username'
    id = Column(db.Integer, primary_key=True)
    forum_id = Column(db.Integer(), index=True, nullable=False, unique=True)
    forum_name = Column(db.String(120), nullable=False)
    # отношения
    user_addr = db.relationship('UserPresents', backref='username_a', cascade="all,delete",
                                foreign_keys='UserPresents.id_user_addressee')
    user_send = db.relationship('UserPresents', backref='username_s',
                                foreign_keys='UserPresents.id_user_sender')
    user_limits = db.relationship('Limits', backref='Limits_uid', cascade="all,delete",
                                  foreign_keys='Limits.user_forum_id')
    notifications = db.relationship('Notifications', backref='username_n', foreign_keys='Notifications.user_id')

    def __repr__(self):
        return '<User %r>' % self.forum_name

    def serialize(self):
        """Метод для сериализации объекта"""
        return {
            "id": self.id,
            "forum_id": self.forum_id,
            "forum_name": self.forum_name
        }


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

    def serialize(self):
        """Метод для сериализации объекта"""
        return {
            "id": self.id,
            "name": self.name,
            "title": self.title,
            "image": self.image,
        }


class UserPresents(db.Model):
    """Подарки пользователей"""
    __tablename__ = 'user_presents'
    id = Column(db.Integer(), primary_key=True)
    id_user_addressee = Column(db.Integer(), db.ForeignKey(Username.forum_id))
    id_user_sender = Column(db.Integer(), db.ForeignKey(Username.forum_id))
    id_present = Column(db.Integer(), db.ForeignKey(Presents.id))
    comment = Column(db.String(500))
    date = Column(db.DateTime(), default=datetime.utcnow)

    # отношения
    time = db.relationship('Notifications', backref='notifications_t', foreign_keys='Notifications.date')

    def serialize(self):
        """Метод для сериализации объекта"""
        return {
            "id": self.id,
            "id_user_addressee": self.id_user_addressee,
            "id_user_sender": self.id_user_sender,
            "id_present": self.id_present,
            "comment": self.comment,
            "date": self.date.strftime("%d.%m.%Y")
        }


class Limits(db.Model):
    """Лимиты на подарки у пользователей"""
    __tablename__ = 'limits'
    id = Column(db.Integer(), primary_key=True)
    user_forum_id = Column(db.Integer(), db.ForeignKey(Username.forum_id))
    limit = Column(db.Integer(), index=True, nullable=False, unique=False)


class Notifications(db.Model):
    """Уведомления"""
    __tablename__ = 'notifications'
    id = Column(db.Integer(), primary_key=True)
    name = Column(db.String(128), index=True)
    user_forum_id = Column(db.Integer(), db.ForeignKey(Username.forum_id))
    date = Column(db.DateTime(), db.ForeignKey(UserPresents.date))

    def serialize(self):
        """Метод для сериализации объекта"""
        return {
            "id": self.id,
            "name": self.name,
            "user_id": self.user_forum_id,
            "date": self.date.strftime("%d.%m.%Y %H:%i")
        }
