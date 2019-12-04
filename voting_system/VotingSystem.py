from flask import Flask
import csv
import datetime

app = Flask(__name__)


# flask run --host=0.0.0.0 fore xternal accesss
# pip freeze > requirements.txt #auto updates all the requirements and the packages


@app.route('/login', method=["POST"])
def login_user():
    return "AA"

def read_candadates(): 
    with open("voting_system/StudentVoters.txt") as f:
        csv_reader = csv.DictReader(f, fieldnames=["name","Registered","dob","id","faculty"])
        
        for line in lines: 
            

@app.route('/')
def hello_world():
    return 'Hello, World!'


def read_candadates():
    return