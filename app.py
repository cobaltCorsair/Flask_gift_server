from flask import Flask, request
from flask_cors import CORS, cross_origin
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)  # объявим экземпляр фласка
cors = CORS(app)  # включаем заголовки для кроссбраузерного ответа
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/getandpost', methods=["POST"])
@cross_origin()
def get_post_javascript_data():
    data = request.data
    print(data)
    return 'Какой-то ответ серверу'


if __name__ == "__main__":
    app.run('0.0.0.0', 5000)  # запустим сервер на 5000 порту
