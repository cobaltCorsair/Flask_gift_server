from datetime import datetime
from models import Username, Presents, UserPresents, db
from sqlalchemy.exc import IntegrityError
import requests


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
                user = Username(forum_name=person_name, forum_id=user_id)
                # чтобы сохранить наш объект user, мы добавляем его в сессию:
                db.session.add(user)
                # сохраняем изменения
                db.session.commit()
                return {'answer': 'Добавлено в бд'}
            else:
                return {'answer': 'Такая запись уже есть'}
        except IntegrityError:
            # откат в случае ошибки (неуникальный id)
            db.session.rollback()

    @staticmethod
    def delete_user(user_id):
        to_delete_user = db.session.query(Username).filter(Username.forum_id == user_id).first()
        if to_delete_user is not None:
            db.session.delete(to_delete_user)
            db.session.commit()
            return {'answer': 'Пользователь удалён'}
        else:
            return {'answer': 'Запись отсутствует в бд'}

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
        return {'answer': 'Добавлено в бд'}

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
            clr_comment = comment.replace("&", "&amp;").replace('"', "&quot;").replace("<", "&lt;").replace(">", "&gt;")
            present = UserPresents(id_user_addressee=addressee, id_user_sender=sender, id_present=id_present,
                                   comment=clr_comment, date=datetime.now())
            db.session.add(present)
            db.session.commit()
            return {'answer': 'Добавлено в бд'}
        except IntegrityError:
            return {'answer': 'Вы пытаетесь добавить несуществующие в базе данных параметры'}

    @staticmethod
    def delete_present(id_present):
        """
        Удаление подарка из списка базы данных
        :param id_present: Идентификатор подарка
        :return: Сообщение об удалении/отсутствии такого подарка
        """
        to_delete_present = db.session.query(Presents).filter(Presents.id == id_present).first()
        if to_delete_present is not None:
            db.session.delete(to_delete_present)
            db.session.commit()
            return {'answer': 'Подарок удалён'}
        else:
            return {'answer': 'Запись отсутствует в базе данных'}

    @staticmethod
    def delete_made_present(id_present):
        """
        Удаление уже сделанного подарка
        :param id_present: Идентификатор подарка
        :return: Сообщение об удалении/отсутствии такого подарка
        """
        to_delete_made_present = db.session.query(UserPresents).filter(UserPresents.id == id_present).first()
        if to_delete_made_present is not None:
            db.session.delete(to_delete_made_present)
            db.session.commit()
            return {'answer': 'Подарок удалён из списка сделанных'}
        else:
            return {'answer': 'Запись отсутствует в базе данных'}

    @staticmethod
    def add_all_users(url):
        """
        Добавляет всех юзеров разом в систему подарков
        :param url: Юрл-адрес, передаваемый из json-запроса
        :return: Оповещение о добавлении
        """
        resp = requests.get(url)
        answer = resp.json()
        for key in answer['response']['users']:
            print(key['username'], key['user_id'])
            UpdateTables.add_new_user(key['username'], key['user_id'])
        return {'answer': 'Все записи добавлены'}


class ViewResults:
    @staticmethod
    def get_user_presents(user_id):
        """
        Функция, получающая подарки пользователя
        :param user_id: идентификатор пользователя
        :return:
        """
        presents = db.session.query(UserPresents, Presents, Username)\
            .join(Presents, UserPresents.id_present == Presents.id)\
            .join(Username, UserPresents.id_user_sender == Username.forum_id)\
            .filter(UserPresents.id_user_addressee == user_id).all()
        if not presents:
            return {'answer': 'Пусто, подарков нет'}
        # возвращаем подарки в словаре из трех словарей
        all_results = {presents.index(i): i for i in presents}
        result = {i: {**x[0].serialize(), **x[1].serialize(), **x[2].serialize()}
                  for i, x in enumerate(all_results.values())}
        print(result)
        return result

    @staticmethod
    def get_all_presents():
        """
        Получаем все подарки базы данных
        :return: Результат запроса
        """
        all_presents = db.session.query(Presents).all()
        if not all_presents:
            return {'answer': 'Подарки еще не были добавлены'}

        all_results = {all_presents.index(i): i.serialize() for i in all_presents}
        return all_results

    @staticmethod
    def get_all_users():
        """
        Получаем всех юзеров системы подарков
        :return: Результат запроса
        """
        all_users = db.session.query(Username).all()
        if not all_users:
            return {'answer': 'Пользователей еще нет'}

        all_results = {all_users.index(i): i.serialize() for i in all_users}
        return all_results

# print(db.session.query(Username).all())
