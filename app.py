from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
cors = CORS(app)  # включаем заголовки для кроссбраузерного ответа


@app.route('/getandpost', methods=["POST"])
@cross_origin()
def get_post_javascript_data():
    data = request.data
    print(data)
    return 'Какой-то ответ серверу'

import models

if __name__ == "__main__":
    app.run('0.0.0.0', 5000)  # запустим сервер на 5000 порту
