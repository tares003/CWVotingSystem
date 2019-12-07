"""
class of student
Students eligible to vote are also stored on a simple text file called StudentVoters.txt. The contents of this file are
simply records, on separate lines, each containing the student user login ID and password name and separated by a
single space or comma.
"""

class Student:
    def __init__(self, first_name, last_name, banner_id, login_id, pwd, has_registered=False):
        self.first_name = first_name
        self.last_name = last_name
        self._login_id = login_id
        self._pwd = pwd
        self.__has_registered = has_registered

    # basic getter and setter methods for registration
    def get_has_registered(self):
        if self.__has_registered:
            print("The student %s %s has registered" % (self.first_name, self.last_name))
        else:
            print("The student %s %s has not registered" % (self.first_name, self.last_name))


    def set_has_registered(self, has_registered):
        self.__has_registered = has_registered  
    
class candadates:
    def __init__(self): 
        self.
    
class gsu_officers(Student): 
   def __init__(self, petitionRunng):

    
    
