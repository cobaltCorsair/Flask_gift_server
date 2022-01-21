# для настройки баз данных
from sqlalchemy import Column, ForeignKey, Integer, String
# для определения таблицы и модели
from sqlalchemy.ext.declarative import declarative_base
# для создания отношений между таблицами
from sqlalchemy.orm import relationship
# для настроек
from sqlalchemy import create_engine

# создание экземпляра declarative_base
Base = declarative_base()

# здесь добавим классы
class Username(Base):
    __tablename__ = 'username'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)

class Presents(Base):
    __tablename__ = 'presents'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    title = Column(String(500), nullable=False)
    image = Column(String(250), nullable=False)

class UserPresents(Base):
    __tablename__ = 'user_presents'
    id = Column(Integer, primary_key=True)
    id_user_addressee = relationship(Username, backref=id)
    id_user_sender = relationship(Username, backref=id)
    id_present = relationship(Presents, backref=id)
    comment = Column(String(500))

# создает экземпляр create_engine в конце файла
engine = create_engine('sqlite:///user_presents.db')
Base.metadata.create_all(engine)