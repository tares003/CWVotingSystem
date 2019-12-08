from flask import Flask
import csv
import datetime
from .models import Student

app = Flask(__name__)


@app.route('/login', method=["POST"])
def login_user():
    return "AA"


@app.route('/')
def hello_world():
    return 'Hello, World!'


def read_candadates():
    return
