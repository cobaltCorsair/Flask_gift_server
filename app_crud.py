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
        :param person_name: имя пользователя
        :param id: идентификатор на форуме
        :return:
        """
        try:
            # проверяем, существует ли такой юзер в бд
            user = db.session.query(Username).filter(Username.forum_id == user_id).all()
            #  если нет, то записываем
            if not user:
                user = Username(name=person_name, forum_id=user_id)
                # Чтобы сохранить наш объект user, мы добавляем его в сессию:
                db.session.add(user)
                # Чтобы сохранить изменения в нашу базу данных и зафиксировать
                # транзакцию, используем commit(). Любое изменение,
                # внесенное для объектов в сессии, не будет сохранено
                # в базу данных, пока не будет вызван session.commit().
                db.session.commit()
                print('Добавлено в бд')

        except IntegrityError:
            # откат в случае ошибки (неуникальный id)
            db.session.rollback()
            print('Такая запись уже есть')
        else:
            # логика добавления другой записи, если id уникален
            pass

    @staticmethod
    def add_new_present(present_name, present_title, image_url):
        """
        Функция для администратора форума, добавляющая подарки в бд
        :param present_name: имя подарка
        :param present_title: описание подарка
        :param image_url: урл картинки
        :return:
        """
        present = Presents(name=present_name, title=present_title, image=image_url)
        db.session.add(present)
        db.session.commit()
        print('Добавлено в бд')

    @staticmethod
    def make_present(addressee, sender, id_present, present_name, comment):
        """
        Функция для администратора форума, добавляющая подарки в бд
        :param comment:
        :param id_present:
        :param addressee: получатель
        :param sender: отправитель
        :param present_name: имя подарка
        :return:
        """
        present = UserPresents(id_user_addressee=addressee, id_user_sender=sender, id_present=id_present,
                               name_present=present_name, comment=comment, date=datetime.now())
        db.session.add(present)
        db.session.commit()
        print('Добавлено в бд')


class ViewResults:
    @staticmethod
    def get_presents_of_user(user_id):
        presents = db.session.query(UserPresents).filter(UserPresents.id_user_addressee == user_id).all()
        for i in presents:
            print(i)
        if not presents:
            print('Пусто, подарков нет')

# print(db.session.query(Username).all())
