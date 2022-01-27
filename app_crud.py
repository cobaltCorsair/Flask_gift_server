from models import Username, db
from sqlalchemy.exc import IntegrityError


def add_new_user(person_name, id):
    try:
        user = Username(name=person_name, forum_id=id)
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


print(db.session.query(Username).all())
