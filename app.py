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
    # добавляем метод записи в бд
    # data = request.data
    if request.method == 'POST':
        name = request.json['Name']
        user_id = request.json['id']
        UpdateTables.add_new_user(name, user_id)
    return 'Запись о пользовател добавлена в базу'


@app.route('/addnewpresent', methods=["POST"])
@cross_origin()
def add_new_present():
    # добавляем метод записи в бд
    # data = request.data
    if request.method == 'POST':
        name = request.json['name']
        title = request.json['title']
        image = request.json['image']
        UpdateTables.add_new_present(name, title, image)
    return 'Подарок успешно добавлен в базу'


@app.route('/getuserpresents', methods=["POST"])
@cross_origin()
def get_user_presents():
    # добавляем метод записи в бд
    # data = request.data
    if request.method == 'POST':
        user_id = request.json['id']
        ViewResults.get_presents_of_user(user_id)
    return 'Подарки пользователя'


if __name__ == "__main__":
    app.run('0.0.0.0', 5000)  # запустим сервер на 5000 порту
