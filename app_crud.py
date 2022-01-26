from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
# импортируем классы Book и Base из файла database_setup.py
from models import Username, Presents, UserPresents

engine = create_engine('sqlite:///user_presents.db')
# Свяжем engine с метаданными класса Base,
# чтобы декларативы могли получить доступ через экземпляр DBSession
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# Экземпляр DBSession() отвечает за все обращения к базе данных
# и представляет «промежуточную зону» для всех объектов,
# загруженных в объект сессии базы данных.
session = DBSession()

try:
    user = Username(name="Moderator", forum_id='2')
    # Чтобы сохранить наш объект user, мы добавляем его в сессию:
    session.add(user)
    # Чтобы сохранить изменения в нашу базу данных и зафиксировать
    # транзакцию, используем commit(). Любое изменение,
    # внесенное для объектов в сессии, не будет сохранено
    # в базу данных, пока не будет вызван session.commit().
    session.commit()
    print('Добавлено в бд')
except IntegrityError:
    # откат в случае ошибки (неуникальный id)
    session.rollback()
    print('Такая запись уже есть')
else:
    # логика добавления другой записи, если id уникален
    pass


print(session.query(Username).all())
