from flask import Flask
import datetime

app = Flask(__name__)


# flask run --host=0.0.0.0 fore xternal accesss
# pip freeze > requirements.txt #auto updates all the requirements and the packages


@app.route('/login', method=["POST"])
def login_user():
    return "AA"

def read_candates: 
    with open("studenvoter.txt") as f:

@app.route('/')
def hello_world():
    return 'Hello, World!'


def read_candadates():
    return