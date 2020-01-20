# This is for starting up the server
from voting_system.VotingSystem import app, read_student_text_file, read_candadates_text_file


# flask run --host=0.0.0.0 fore external access
# pip freeze > requirements.txt #auto updates all the requirements and the packages


# TODO: Make that a gui of starting server + Loading the text file of students + candidates
def tk_gui():
    pass


if __name__ == "__main__":

    app.config.from_object("config.DevelopmentConfig")

    read_student_text_file('voting_system/RandomStudents.csv', remove_dups=True)
    read_candadates_text_file('voting_system/RandomCandidates.csv', remove_dups=True)

    # Can use cfg files by parsing as VOTINGSYS_SETTINGS=path/to/Config/file.cfg
    # overrides the the setting from the previous setting
    try:
        app.config.from_envvar('APP_CONFIG_FILE')
    except RuntimeError:
        pass
    except:
        pass
    app.run(port=2222)