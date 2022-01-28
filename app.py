from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
cors = CORS(app)  # включаем заголовки для кроссбраузерного ответа

from app_crud import add_new_user

@app.route('/getandpost', methods=["POST"])
@cross_origin()
def get_post_javascript_data():
    # добавляем метод записи в бд
    data = request.data
    if request.method == 'POST':
        name = request.json['Name']
        id = request.json['id']
        add_new_user(name, id)
    return 'Какой-то ответ серверу'


if __name__ == "__main__":
    app.run('0.0.0.0', 5000)  # запустим сервер на 5000 порту
