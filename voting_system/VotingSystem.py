import csv
from datetime import datetime, timedelta
from functools import wraps

from flask import Flask, flash
from flask import request, render_template, redirect, url_for
from flask_login import login_user, LoginManager, login_required, logout_user, current_user
from flask_restplus import reqparse

from .models import Student, Candidate

app = Flask(__name__, template_folder="templates")
# For managing logins
login_manager = LoginManager()
login_manager.init_app(app)

ALL_STUDENTS = []  # storing all the student from the text file
ALL_CANDIDATES = []  # storing all the candidates from the text file


# https://flask-login.readthedocs.io/en/latest/#how-it-works


@login_manager.user_loader
def load_user(user_id):
    return get_student_by_id(user_id)


def get_cadidates_by_position(position):
    global ALL_CANDIDATES
    candidates = []
    for candidate in ALL_CANDIDATES:
        if candidate.position.lower() == position.lower():
            candidates.append(candidate)
    if candidates:
        return candidates
    else:
        return False


def check_within_timeframe(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if app.config["VOTING_START_DATE"] & app.config["VOTING_END_DATE"]:
            timenow = datetime.now().timestamp()
            if timenow >= app.config["VOTING_START_DATE"].timestamp() and timenow <= app.config[
                "VOTING_END_DATE"].timestamp():
                return func(*args, **kwargs)
            else:
                return "Voting Time  Expired"
        else:
            print("Start and End Date not provided")

    return decorated_function


def get_student_by_id(student_id):
    """

    Returns Student with the specified id
    :param student_id:
    :return:
    """
    global ALL_STUDENTS
    for student in ALL_STUDENTS:
        if student.get_user_id() == student_id:
            return student
    return False


def map_the_objects(class_to_map_to, iterable):
    """
    This maps line to an  class
    :param class_to_map_to: Class eg Student
    :param iterable: iterable- needs to be dict
    :return: list containing all the objects
    """
    return [class_to_map_to(**dict(details_row)) for details_row in iterable]


# TODO: Umar
def remove_duplicates(candidates=False):
    ALl_Unique_Cadidates = []
    if candidates:
        global ALL_CANDIDATES
        for candidate in ALL_CANDIDATES:
            pass

        # this is if they are candidate
    else:
        pass
        # not candidate


def read_student_text_file():
    with open('voting_system/RandomStudents.csv', 'r') as student_file:
        required_fields_in_csv_file = ["name", "has_registered", "dob", "login_id", "faculty",
                                       "password", 'directory_to_user_image']
        # TODO: Remove  Duplicate students
        csv_reader = csv.DictReader(student_file,
                                    fieldnames=required_fields_in_csv_file)

        global ALL_STUDENTS
        ALL_STUDENTS = map_the_objects(Student, csv_reader)


def read_candadates_text_file():
    with open("voting_system/RandomCandidates.csv") as candidate_file:
        required_fields_in_csv_file = ["name", "has_registered", "dob", "login_id",
                                       "position", "faculty", "password",
                                       'campaign', 'promises', 'logoref']  # logoref - contain ref directory of img
        csv_reader = csv.DictReader(candidate_file,
                                    fieldnames=required_fields_in_csv_file)

        global ALL_CANDIDATES

        ALL_CANDIDATES = map_the_objects(Candidate, csv_reader)


logindetailsPasrsing = reqparse.RequestParser()
logindetailsPasrsing.add_argument('student_id', type=str, required=True, help='No Student ID Provided')
logindetailsPasrsing.add_argument('password', type=str, required=True, help='No password Provided')


@app.route('/login', methods=["POST", "GET"])
def login():
    if request.method == "POST":

        args = logindetailsPasrsing.parse_args()
        matched_student = get_student_by_id(args['student_id'])

        if matched_student:
            if matched_student.verify_password(
                    args["password"]) & matched_student.is_registered():  # checking password is valid
                login_user(matched_student, timedelta(minutes=10))  # 10 minutes after the cookie will expire
                flash('You were successfully logged in')
                return redirect(url_for('selection', position="president"))
            else:
                return "Password not valid OR you are not registered", 404
        else:
            return '%s is not eligible to vote' % args['student_id'], 404
    else:
        return render_template("login.html")


@app.route("/logout", methods=["GET"])
@login_required
def logout():
    """Logout the current user."""
    user = current_user
    print(current_user.__dict__)
    user.authenticated = False
    logout_user()
    return render_template("logout.html")


@app.route('/')
def hello_world():
    return render_template("welcomePage.html")


@app.route('/selection/<position>')
@login_required
def selection(position):
    # TODO Check if they already Voted 
    position = position.lower()
    if position:
        candidates = get_cadidates_by_position(position)
        if candidates:
            #print(current_user.__dict__)
            print(current_user.get_user_faculty())
            if position == 'faculty officer':
                faculty_candidates = list(filter(lambda x: x.get_user_faculty() == current_user.get_user_faculty(),
                                            candidates))
                #print(faculty_candidates[0].__dict__)
                return render_template("selection.html", candidates=faculty_candidates)
            else:
                return render_template("selection.html", candidates=candidates)

        else:
            return "No Candidates for this %s position " % position
    else:
        return "position not provided"


def view_all_results():
    # TODO returns all the results in json format
    pass
