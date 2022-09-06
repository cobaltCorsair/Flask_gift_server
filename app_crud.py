from datetime import datetime
from models import Username, Presents, UserPresents, Limits, Notifications, db
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func
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
            if len(person_name) != 0 and int(user_id) > 0:
                try:
                    # проверяем, существует ли такой юзер в бд
                    user = db.session.query(Username).filter(Username.forum_id == user_id).all()
                    #  если нет, то записываем
                    if not user:
                        user = Username(forum_name=person_name, forum_id=user_id)
                        # чтобы сохранить наш объект user, мы добавляем его в сессию:
                        db.session.add(user)
                        UpdateTables.limit_for_user(user_id)
                        # сохраняем изменения
                        db.session.commit()
                        return {'answer': 'Добавлено в базу данных'}
                    else:
                        return {'answer': 'Такая запись уже есть'}
                except IntegrityError:
                    # откат в случае ошибки (неуникальный id)
                    db.session.rollback()
            else:
                return {'answer': 'Заполните необходимые поля!'}
        except TypeError:
            return {'answer': 'Идентификатор должен быть числом, а имя - не пустым!'}

    @staticmethod
    def delete_user(user_id):
        to_delete_user = db.session.query(Username).filter(Username.forum_id == user_id).first()
        if to_delete_user is not None:
            db.session.delete(to_delete_user)
            db.session.commit()
            return {'answer': 'Пользователь удалён'}
        else:
            return {'answer': 'Запись отсутствует в базе данных'}

    @staticmethod
    def add_new_present(present_name, present_title, image_url):
        """
        Функция для администратора форума, добавляющая подарки в бд
        :param present_name: имя подарка
        :param present_title: описание подарка
        :param image_url: url картинки
        :return:
        """
        if len(present_name) != 0 and len(image_url) != 0:
            present = Presents(name=present_name, title=present_title, image=image_url)
            db.session.add(present)
            db.session.commit()
            return {'answer': 'Добавлено в базу данных'}
        else:
            return {'answer': 'Заполните необходимые поля!'}

    @staticmethod
    def make_present(addressee, sender, id_present, comment):
        """
        Функция, позволяющая добавлять подарки определенному пользователю
        :param comment: комментарий
        :param id_present: id подарка
        :param addressee: получатель
        :param sender: отправитель
        :return:
        """
        date_send = datetime.now()
        get_lim = db.session.query(Limits.limit).filter(Limits.user_forum_id == sender).first()
        if get_lim[0] > 0:
            try:
                clr_comment = comment.replace("&", "&amp;").replace('"', "&quot;").replace("<", "&lt;").replace(">",
                                                                                                                "&gt;")
                present = UserPresents(id_user_addressee=addressee, id_user_sender=sender, id_present=id_present,
                                       comment=clr_comment, date=date_send)
                db.session.add(present)
                # изменяем лимит
                UpdateTables.reduction_limit(sender)
                # добавляем новое уведомление
                UpdateTables.add_notification(addressee=addressee, sender=sender, date=date_send)
                # сохраняем изменения
                db.session.commit()
                return {'answer': 'Подарок успешно отправлен'}
            except IntegrityError:
                return {'answer': 'Вы пытаетесь использовать несуществующие в базе данных параметры'}
        else:
            return {'answer': 'Вы превысили суточный лимит отправки подарков'}

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
    def edit_present(id_present, p_name, p_title, p_image):
        """
        Редактирование уже добавленного в базу подарка
        :param image: Картинка подарка
        :param title: Описание подарка
        :param name: Имя подарка
        :param id_present: Идентификатор подарка
        :return: Сообщение об изменении/отсутствии такого подарка
        """
        to_edit_present = db.session.query(Presents).filter(Presents.id == id_present)
        if to_edit_present is not None:
            to_edit_present.update({
                Presents.name: p_name,
                Presents.title: p_title,
                Presents.image: p_image,
            }, synchronize_session=False)
            db.session.commit()
            return {'answer': 'Подарок успешно изменён'}
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
            UpdateTables.add_new_user(key['username'], key['user_id'])
        return {'answer': 'Все записи добавлены'}

    @staticmethod
    def limit_for_user(user_id):
        """
        Добавляем юзера в таблицу с лимитами
        :param user_id: Идентификатор пользователя
        :return:
        """
        limits = Limits(user_forum_id=user_id, limit=5)
        db.session.add(limits)

    @staticmethod
    def update_limits_everyday():
        """
        Обновляем лимиты
        :return:
        """
        db.session.query(Limits).update({
            Limits.limit: 5,
        }, synchronize_session=False)
        # сохраняем изменения
        db.session.commit()
        return {'answer': 'Лимиты обновлены'}

    @staticmethod
    def reduction_limit(user_id):
        """
        Уменьшаем лимит на единицу
        :param user_id: Идентификатор пользователя
        :return:
        """
        db.session.query(Limits).filter(Limits.user_forum_id == user_id).update({
            Limits.limit: Limits.limit - 1,
        }, synchronize_session=False)

    @staticmethod
    def rename_user(user_id, new_name):
        """
        Переименовываем пользователя
        :param user_id: идентификатор пользователя
        :param new_name: новое имя пользователя
        :return:
        """
        user_to_rename = db.session.query(Username).filter(Username.forum_id == user_id)
        if user_to_rename.first() is not None:
            user_to_rename.update({
                Username.forum_name: new_name,
            }, synchronize_session=False)
            db.session.commit()
            return {'answer': 'Имя пользователя обновлено'}
        else:
            return {'answer': 'Такого пользователя нет в списке'}

    @staticmethod
    def add_notification(addressee, sender, date):
        """
        Добавляем уведомления об отправке подака пользоателю
        :param addressee: получатель
        :param sender: отправитель
        :param date: дата
        :return:
        """
        # предварительно удаляем такое же оповещение, если оно есть
        db.session.query(Notifications).filter(id_user_addressee=addressee, id_user_sender=sender,
                                               date=date).delete()
        notification = Notifications(id_user_addressee=addressee, id_user_sender=sender, date=date)
        db.session.add(notification)


class ViewResults:
    @staticmethod
    def get_user_presents(user_id):
        """
        Функция, получающая подарки пользователя
        :param user_id: идентификатор пользователя
        :return:
        """
        presents = db.session.query(UserPresents, Presents, Username) \
            .join(Presents, UserPresents.id_present == Presents.id) \
            .join(Username, UserPresents.id_user_sender == Username.forum_id) \
            .filter(UserPresents.id_user_addressee == user_id).all()
        if not presents:
            return {'answer': 'Пусто, подарков нет'}
        # возвращаем подарки в словаре из трех словарей
        all_results = {presents.index(i): i for i in presents}
        result = {i: {**x[1].serialize(), **x[2].serialize(), **x[0].serialize()}
                  for i, x in enumerate(all_results.values())}
        return result

    @staticmethod
    def get_all_presents():
        """
        Получаем все подарки базы данных
        :return: Результат запроса
        """
        all_presents = db.session.query(Presents).all()
        if not all_presents:
            return {'answer': 'Подарки ещё не были добавлены'}

        all_results = {all_presents.index(i): i.serialize() for i in all_presents}
        return all_results

    @staticmethod
    def get_edit_present(id_present):
        """
        Выдача данных подарка из списка базы данных
        :param id_present: Идентификатор подарка
        :return: Сообщение о результате или отсутствии такого подарка
        """
        to_edit_present = db.session.query(Presents).filter(Presents.id == id_present).first()
        if not to_edit_present:
            return {'answer': 'Запись отсутствует в базе данных'}
        else:
            result = to_edit_present.serialize()
            return result

    @staticmethod
    def get_all_users():
        """
        Получаем всех юзеров системы подарков
        :return: Результат запроса
        """
        all_users = db.session.query(Username).order_by(Username.forum_name).all()
        if not all_users:
            return {'answer': 'Пользователей ещё нет'}

        all_results = {all_users.index(i): i.serialize() for i in all_users}
        return all_results

    @staticmethod
    def get_presents_count():
        """
        Получаем количество подарков пользователя
        :return:
        """
        presents_count = db.session.query(UserPresents.id_user_addressee, func.count(UserPresents.id)). \
            group_by(UserPresents.id_user_addressee).all()
        presents_count = {i[0]: i[1] for i in presents_count}
        if presents_count is not None:
            return {'answer': presents_count}
        else:
            return {'answer': 0}
