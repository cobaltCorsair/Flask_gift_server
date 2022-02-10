from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
cors = CORS(app)  # включаем заголовки для кроссбраузерного ответа

if 'sqlite' in app.config['SQLALCHEMY_DATABASE_URI']:
    def _fk_pragma_on_connect(dbapi_con, con_record):
        """Включаем поддержку внешних ключей"""
        dbapi_con.execute('pragma foreign_keys=ON')

    with app.app_context():
        from sqlalchemy import event
        event.listen(db.engine, 'connect', _fk_pragma_on_connect)

from app_crud import UpdateTables, ViewResults


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
        name = request.json['name']
        user_id = request.json['id']
        request_result = UpdateTables.add_new_user(name, user_id)
        return request_result


@app.route('/addnewpresent', methods=["POST"])
@cross_origin()
def add_new_present():
    """
    Пополняем базу подарков
    :return:
    """
    # добавляем метод записи в бд
    # data = request.data
    if request.method == 'POST':
        name = request.json['name']
        title = request.json['title']
        image = request.json['image']
        request_result = UpdateTables.add_new_present(name, title, image)
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
    if request.method == 'POST':
        id = request.json['id']
        request_result = UpdateTables.delete_present(id)
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


if __name__ == "__main__":
    app.run('0.0.0.0', 5000)  # запустим сервер на 5000 порту
