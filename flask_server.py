# This is for starting up the server
from voting_system.VotingSystem import app, read_student_text_file, read_candadates_text_file


# flask run --host=0.0.0.0 fore external access
# pip freeze > requirements.txt #auto updates all the requirements and the packages


# TODO: Make that a gui of starting server + Loading the text file of students + candidates
def tk_gui():
    pass

# TODO: Get the vote selction
# TODO: Store it in local DB
# TODO: Count vote with tie considaration
# todo:

# import pandas
# import re
#
# pd_df = pandas.read_csv('fred.csv', header=0)
#
# def filter_by_position(position):
#     return pd_df[pd_df.position.str.lower() == position.lower()]
#
#
# def sort_by_cadidates(df):
#     return df.sort_values(['first_votes','second_votes','third_votes','fourth_votes'], ascending=[True, True, True, True])
#
#
#
# user_fileter = str(input('Enter the position to filter by:'))
#
# ##print(filter_by_position('President'))
#
# filtered = filter_by_position(user_fileter)
# print(sort_by_cadidates(filtered))
# #
# # print(pd_df[pd_df.position == 'President'])


if __name__ == "__main__":
    app.config.from_object("config.DevelopmentConfig")
    read_student_text_file('RandomStudents.csv', remove_dups=True)
    read_candadates_text_file('RandomCandidates.csv', remove_dups=True)

    # Can use cfg files by parsing as VOTINGSYS_SETTINGS=path/to/Config/file.cfg
    # overrides the the setting from the previous setting
    try:
        app.config.from_envvar('APP_CONFIG_FILE')
    except RuntimeError:
        pass
    except:
        pass
    app.run(port=2222)
