from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
cors = CORS(app)  # включаем заголовки для кроссбраузерного ответа

from app_crud import UpdateTables, ViewResults


@app.route('/addnewuser', methods=["POST"])
@cross_origin()
def get_post_javascript_data():
    """
    Добавляем юзера в бд
    :return:
    """
    # добавляем метод записи в бд
    # data = request.data
    if request.method == 'POST':
        name = request.json['name']
        user_id = request.json['id']
        UpdateTables.add_new_user(name, user_id)
    return 'Запись о пользователе добавлена в базу'


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
        UpdateTables.add_new_present(name, title, image)
    return 'Подарок успешно добавлен в базу'


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
        present_name = request.json['present_name']
        comment = request.json['comment']
        UpdateTables.make_present(addressee, sender, id_present, present_name, comment)
    return 'Подарок успешно отправлен'


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
        ViewResults.get_presents_of_user(user_id)
    return 'Подарки пользователя'


if __name__ == "__main__":
    app.run('0.0.0.0', 5000)  # запустим сервер на 5000 порту
