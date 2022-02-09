from datetime import datetime

from models import Username, Presents, UserPresents, db
from sqlalchemy.exc import IntegrityError


class UpdateTables:
    """
    Класс, добавляющий данные в базу
    """

    @staticmethod
    def add_new_user(person_name, user_id):
        """
        Добавляет нового пользователя в список пользователей системы подарков
        :param user_id: идентификатор на форуме
        :param person_name: имя пользователя
        :return:
        """
        try:
            # проверяем, существует ли такой юзер в бд
            user = db.session.query(Username).filter(Username.forum_id == user_id).all()
            #  если нет, то записываем
            if not user:
                user = Username(name=person_name, forum_id=user_id)
                # чтобы сохранить наш объект user, мы добавляем его в сессию:
                db.session.add(user)
                # сохраняем изменения
                db.session.commit()
                return 'Добавлено в бд'
            else:
                return 'Такая запись уже есть'
        except IntegrityError:
            # откат в случае ошибки (неуникальный id)
            db.session.rollback()
        finally:
            # логика добавления другой записи после проверок на существование юзера
            # TODO: нужна логика на случай отсутствия в базе не только отправителя, но и адресата!
            # TODO: или вызвать эту функцию дважды для проверки и отправителя, и адресата
            print('Можно добавить запись о подарке')

    @staticmethod
    def add_new_present(present_name, present_title, image_url):
        """
        Функция для администратора форума, добавляющая подарки в бд
        :param present_name: имя подарка
        :param present_title: описание подарка
        :param image_url: url картинки
        :return:
        """
        present = Presents(name=present_name, title=present_title, image=image_url)
        db.session.add(present)
        db.session.commit()
        return 'Добавлено в бд'

    @staticmethod
    def make_present(addressee, sender, id_present, comment):
        """
        Функция, позволяющая добавлять подарки определенному пользователю
        :param comment:
        :param id_present:
        :param addressee: получатель
        :param sender: отправитель
        :return:
        """
        try:
            present = UserPresents(id_user_addressee=addressee, id_user_sender=sender, id_present=id_present,
                                   comment=comment, date=datetime.now())
            db.session.add(present)
            db.session.commit()
            return 'Добавлено в бд'
        except IntegrityError:
            return 'Вы пытаетесь добавить несуществующие в бд параметры'


class ViewResults:
    @staticmethod
    def get_user_presents(user_id):
        """
        Функция, получающая подарки пользователя
        :param user_id: идентификатор пользователя
        :return:
        """
        presents = db.session.query(UserPresents).filter(UserPresents.id_user_addressee == user_id).all()
        for i in presents:
            return i
        if not presents:
            return 'Пусто, подарков нет'

# print(db.session.query(Username).all())
