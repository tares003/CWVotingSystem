import csv
import sys
from datetime import datetime, timedelta
from functools import wraps

from flask import Flask, flash
from flask import request, render_template, redirect, url_for
from flask_login import login_user, LoginManager, login_required, logout_user, current_user
from flask_restplus import reqparse
from prettytable import PrettyTable

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
    #method  for the login manager
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
    next(iterable) #removes the first line
    return [class_to_map_to(**dict(details_row)) for details_row in iterable]


def get_users_with_matching_hash(searching_hash, list_of_objects):
    """
        returns all the user with matching hash
        :param searching_hash: hash to search for
        :param list_of_objects: objects with hash implemented
    """
    return list(filter(lambda x: hash(x) == searching_hash, list_of_objects))


def list_all_duplicates(iterable):
    """
    Returns the duplicates of an objects of an iterable
    """
    already_seen = set()
    seen_twice = set(x for x in iterable if x in already_seen or already_seen.add(
        x))  # adds already seen or keeps it if appeared more than  2 times

    return list(seen_twice)


def dups_removal_selction(list_of__dups_usr_Objects, table_column, original_List):
    """
    creates
    """
    table = PrettyTable(table_column)
    for idx, list_of_usr_Object in enumerate(list_of__dups_usr_Objects):
        row = list(list_of_usr_Object.get_user_ppi_info())
        row.insert(0, str(idx))
        table.add_row(row)

    valid = False
    selections = None
    print('Number of USers in original list %s ' % len(original_List))
    while not valid:
        try:
            print("Please enter the the userid which you want to keep")
            selections = int(input(table))
            if 0 <= selections <= len(list_of__dups_usr_Objects) - 1:
                print("Selected ID %s \n removed user %s " % (
                selections, str(list_of__dups_usr_Objects[selections].get_user_ppi_info())))
                valid = True
                for i in range(len(list_of__dups_usr_Objects)):  # removing all others except selected one
                    if i == selections:
                        continue
                    original_List.remove(list_of__dups_usr_Objects[selections])  # removes from the original list

                print('Number of users in original list after Removal %s ' % len(original_List))

            else:
                print('%s is NOT VALID userid, please enter a valid id' % selections)
        except ValueError:
            print('Only number allowed')
        except Exception:
            print('ERROR Removing Duplicates')
            import traceback
            traceback.print_exc()
            sys.exit()

    # Can be used if you want to be removed by user id
    # while not valid:
    #     print("Please enter the the userid which you want to keep")
    #     selections = str(input(table))
    #     for list_of_usr_Object in list_of__dups_usr_Objects:  # checking if id is valid
    #         if list_of_usr_Object.get_id().lower() == selections.lower():
    #             print("Selected userID %s" % selections)
    #             valid = True
    #     else:
    #         print('NOT VALID userid')

    # This is Exta allows user to select user which they want to remove
    # while not valid:
    #     selctions = str(input("Please enter the the userid which you what to be removed, if more than "
    #                           "than 2 use comma to separate them eg")).split(',')
    #     for selction in selctions:
    #         # checking if given userid in valid and are from these dups and return would be one user which to keeep
    #         if len([selection.lower() for selection in selctions
    #                 if selection in [usr.get_id().lower() for usr in list_of__dups_usr_Objects]
    #                 ]) == len(selction)-1: #checking with all the object that matches the
    #             valid = True


# TODO: Umar
def remove_duplicates(list_of_user_object):
    """
    Removes the duplicate user
    """
    if not list_of_user_object:
        print('Empty list')
        return None
    all_candidates_hash = [hash(candidates) for candidates in list_of_user_object]  # all the hash set
    all_duplicates_hashes = list_all_duplicates(all_candidates_hash)
    # for user in list_of_user_object:
    #     c_hash = hash(user)
    #     if c_hash in all_candidates_hash and all_candidates_hash.count(c_hash) > 1:
    if all_duplicates_hashes:
        for dup_hash in all_duplicates_hashes:
            print('found duplicate')
            table_cols = ['id', 'first name', 'dob', 'login id', 'faculty']
            dups_users_with_this_hash = get_users_with_matching_hash(dup_hash, list_of_user_object)
            # using 1st object is check object type
            if isinstance(dups_users_with_this_hash[0], Candidate):
                dups_removal_selction(dups_users_with_this_hash, table_cols.append('position'),
                                      list_of_user_object)  # extra col for cadidates
            elif isinstance(dups_users_with_this_hash[0], Student):
                dups_removal_selction(dups_users_with_this_hash, table_cols, list_of_user_object)
            else:
                dups_removal_selction(dups_users_with_this_hash, [], list_of_user_object)
    else:
        print('NO Duplicates found')


def read_student_text_file(text_file_name, remove_dups = False):
    with open(text_file_name, 'r') as student_file:
        required_fields_in_csv_file = ["name", "has_registered", "dob", "login_id", "faculty",
                                       "password", 'directory_to_user_image']
        # TODO: Remove  Duplicate students
        csv_reader = csv.DictReader(student_file,
                                    fieldnames=required_fields_in_csv_file)

        global ALL_STUDENTS
        ALL_STUDENTS = map_the_objects(Student, csv_reader)
        if remove_dups:
            remove_duplicates(ALL_STUDENTS)


def read_candadates_text_file(text_file_name,remove_dups = False):
    with open(text_file_name) as candidate_file:
        required_fields_in_csv_file = ["name", "has_registered", "dob", "login_id",
                                       "position", "faculty", "password",
                                       'campaign', 'promises', 'logoref']  # logoref - contain ref directory of img
        csv_reader = csv.DictReader(candidate_file,
                                    fieldnames=required_fields_in_csv_file)

        global ALL_CANDIDATES

        ALL_CANDIDATES = map_the_objects(Candidate, csv_reader)
        if remove_dups:
            remove_duplicates(ALL_CANDIDATES)


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
                print('Success')
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

    if request.method == 'GET':
        position = position.lower()
        if position:
            candidates = get_cadidates_by_position(position)
            if candidates:
                # print(current_user.__dict__)
                print(current_user.get_user_faculty())
                if position == 'faculty officer':
                    #Filter out so only returns student's  faculty.
                    candidates = list(filter(lambda x: x.get_user_faculty() == current_user.get_user_faculty(),
                                                     candidates))

                    # print(faculty_candidates[0].__dict__)

                candidates = {position: candidates}

                return render_template("selection.html", candidates=candidates)

            else:
                return "No Candidates for this %s position " % position
        else:
            return "position not provided"

    elif request.method == 'POST':
        pass

# @app.route('/selection/<position>')
# @login_required
# def users_vote():
#     pass




def view_all_results():
    # TODO returns all the results in json format
    pass
