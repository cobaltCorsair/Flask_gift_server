from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
cors = CORS(app)  # включаем заголовки для кроссбраузерного ответа

if 'sqlite' in app.config['SQLALCHEMY_DATABASE_URI']:
    def _fk_pragma_on_connect(dbapi_con, con_record):
        """Включаем поддержку внешних ключей"""
        dbapi_con.execute('pragma foreign_keys=ON')
        dbapi_con.execute("pragma journal_mode=wal;")


    with app.app_context():
        from sqlalchemy import event

        event.listen(db.engine, 'connect', _fk_pragma_on_connect)

from app_crud import UpdateTables, ViewResults


@app.route('/')
def start_app():
    return 'Сервер успешно запущен!'


@app.route('/addnewuser', methods=["POST"])
@cross_origin()
def add_new_user():
    """
    Добавляем юзера в бд
    :return:
    """
    # добавляем метод записи в бд
    # data = request.data
    if request.method == 'POST':
        forum_name = request.json['forum_name']
        user_id = request.json['id']
        request_result = UpdateTables.add_new_user(forum_name, user_id)
        return request_result


@app.route('/deleteuser', methods=["POST"])
@cross_origin()
def delete_user():
    """
    Удаляем пользователя из бд
    :return:
    """
    if request.method == 'POST':
        id = request.json['forum_id']
        request_result = UpdateTables.delete_user(id)
        return request_result


@app.route('/addnewpresent', methods=["POST"])
@cross_origin()
def add_new_present():
    """
    Пополняем базу подарков
    :return:
    """
    # добавляем метод записи в бд
    if request.method == 'POST':
        name = request.json['name']
        title = request.json['title']
        image = request.json['image']
        request_result = UpdateTables.add_new_present(name, title, image)
        return request_result


@app.route('/editpresent', methods=["POST"])
@cross_origin()
def edit_present():
    """
    Редактируем базу подарков
    :return:
    """
    # добавляем метод записи в бд
    if request.method == 'POST':
        id = request.json['id']
        name = request.json['name']
        title = request.json['title']
        image = request.json['image']
        request_result = UpdateTables.edit_present(id, name, title, image)
        return request_result


@app.route('/makepresent', methods=["POST"])
@cross_origin()
def make_present():
    """
    Отправляем подарок
    :return:
    """
    # добавляем метод записи в бд
    # data = request.data
    if request.method == 'POST':
        addressee = request.json['addressee']
        sender = request.json['sender']
        id_present = request.json['id_present']
        comment = request.json['comment']
        request_result = UpdateTables.make_present(addressee, sender, id_present, comment)
        return request_result


@app.route('/deletepresent', methods=["POST"])
@cross_origin()
def delete_present():
    """
    Удаляем подарок из базы
    :return:
    """
    if request.method == 'POST':
        id = request.json['id']
        request_result = UpdateTables.delete_present(id)
        return request_result


@app.route('/geteditpresent', methods=["POST"])
@cross_origin()
def get_edit_present():
    """
    Получаем подарок для редактирования
    :return:
    """
    if request.method == 'POST':
        id = request.json['id']
        request_result = ViewResults.get_edit_present(id)
        return request_result


@app.route('/deletemadepresent', methods=["POST"])
@cross_origin()
def delete_made_present():
    """
    Удаляем сделанный подарок
    :return:
    """
    if request.method == 'POST':
        id = request.json['id']
        request_result = UpdateTables.delete_made_present(id)
        return request_result


@app.route('/addallusers', methods=["POST"])
@cross_origin()
def add_all_users():
    """
    Записываем в бд всех юзеров через запрос к апи
    :return:
    """
    if request.method == 'POST':
        url = request.json['url']
        request_result = UpdateTables.add_all_users(url)
        return request_result


@app.route('/getuserpresents', methods=["POST"])
@cross_origin()
def get_user_presents():
    """
    Получаем все подарки пользователя
    :return:
    """
    # добавляем метод записи в бд
    # data = request.data
    if request.method == 'POST':
        user_id = request.json['id']
        request_result = ViewResults.get_user_presents(user_id)
        return request_result


@app.route('/getallpresents', methods=["POST"])
@cross_origin()
def get_all_presents():
    """
    Получаем все существующие в базе подарки, доступные для дарения
    :return:
    """
    if request.method == 'POST':
        request_result = ViewResults.get_all_presents()
        return request_result


@app.route('/getallusers', methods=["POST"])
@cross_origin()
def get_all_users():
    """
    Получаем всех существующих в базе пользователей, которым можно дарить подарки
    :return:
    """
    if request.method == 'POST':
        request_result = ViewResults.get_all_users()
        return request_result


@app.route('/getpresentscount', methods=["POST"])
@cross_origin()
def get_presents_count():
    """
    Получаем количество подарков пользователя
    :return:
    """
    if request.method == 'POST':
        request_result = ViewResults.get_presents_count()
        return request_result


@app.route('/resetlimits', methods=["POST"])
@cross_origin()
def reset_limits_by_hand():
    """
    Сбрасываем лимиты вручную, добавляет 5 попыток дарения подарков всем юзерам
    :return:
    """
    if request.method == 'POST':
        request_result = UpdateTables.update_limits_everyday()
        return request_result


@app.route('/renameuser', methods=["POST"])
@cross_origin()
def rename_user():
    """
    Переименовываем пользователя в таблице пользователей
    :return:
    """
    if request.method == 'POST':
        user_id = request.json['forum_id']
        new_name = request.json['new_name']
        request_result = UpdateTables.rename_user(user_id, new_name)
        return request_result


def reset_limits():
    """
    Ежесуточный сброс лимитов по таймеру
    :return:
    """
    UpdateTables.update_limits_everyday()


sheduler = BackgroundScheduler({'apscheduler.timezone': 'Europe/Moscow'})
sheduler.add_job(reset_limits, 'interval', hours=24)
sheduler.start()

if __name__ == "__main__":
    app.run()  # запустим сервер
