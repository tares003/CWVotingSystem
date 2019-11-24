from flask import Flask
app = Flask(__name__)

#flask run --host=0.0.0.0 fore xternal accesss
#pip freeze > requirements.txt #auto updates all the requirements and the packages


@app.route('/')
def hello_world():
    return 'Hello, World!'


def

