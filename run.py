# This is for starting up the server
from voting_system.VotingSystem import app
from voting_system.models import Student, Candidate
import csv

# flask run --host=0.0.0.0 fore external access
# pip freeze > requirements.txt #auto updates all the requirements and the packages
ALL_STUDENTS = []  # storing all the student from the text file
ALL_CANDIDATES = []  # storing all the candidates from the text file


def map_the_objects(class_to_map_to, iterable):
    """
    This maps line to an  class
    :param class_to_map_to: Class eg Student
    :param iterable: iterable- needs to be dict
    :return: list containing all the objects
    """
    return [class_to_map_to(**dict(details_row)) for details_row in iterable]

# TODO: Umar
def remove_duplicates(candadates=False):
    if candadates:
        pass
        # this is if they are candidate
    else:
        pass
        # not candidate


def read_student_text_file():
    with open('RandomStudents.csv', 'r') as student_file:
        # TODO: Remove  Duplicate students
        csv_reader = csv.DictReader(student_file,
                                    fieldnames=["name", "has_registered", "dob", "login_id", "faculty", "password"])

        global ALL_STUDENTS
        ALL_STUDENTS = map_the_objects(Student, csv_reader)


def read_candadates():
    with open("RandomCandidates.csv") as candidate_file:
        csv_reader = csv.DictReader(candidate_file,
                                    fieldnames=["name", "Registered", "dob", "id", "position", "faculty", "password"])

        global ALL_STUDENTS

        ALL_STUDENTS = map_the_objects(Candidate, csv_reader)


# TODO: Make that a gui of starting server + Loading the text file of students + candadates
def tk_gui():
    pass


if __name__ == "__main__":
    app.config.from_object("config.DevelopmentConfig")

    # Can use cfg files by parsing as VOTINGSYS_SETTINGS=path/to/Config/file.cfg
    # overrides the the setting from the previous setting
    try:
        app.config.from_envvar('APP_CONFIG_FILE')
    except RuntimeError:
        pass
    except:
        pass
    app.run(port=2222)
