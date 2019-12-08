"""
class of student
Students eligible to vote are also stored on a simple text file called StudentVoters.txt. The contents of this file are
simply records, on separate lines, each containing the student user login ID and password name and separated by a
single space or comma.
"""


class login_management:
    def __init__(self):
        self.authenticated =False;

    #https://flask-login.readthedocs.io/en/latest/#how-it-works Doc
    def is_active(self):
        """Returns True as all the users in text file is active"""
        return True

    def get_id(self):
        """Return the Student id- required by the module"""
        return self.email

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated

    def is_anonymous(self):
        """False, as anonymous Student aren't supported."""
        return False


class Student(login_management):
    def __init__(self, name, login_id, password, dob, faculty, has_registered=False):
        self.first_name = name.split()[0]
        self.middle_name = " ".join(name.split()[1:len(name.split()) - 1])  # gets all the middle names
        self.last_name = name.split()[-1]
        self._login_id = login_id
        self._faculty = faculty
        self.email_name = self.first_name[
                              0] + self.last_name  # This property could be used to send out email after vote been casted
        self.__pwd = password
        self.dob = dob
        self.__has_registered = has_registered

    # check if user is registered
    def get_has_registered(self):
        if self.__has_registered:
            print("The student %s %s has registered" % (self.first_name, self.last_name))
            return True
        else:
            print("The student %s %s has not registered" % (self.first_name, self.last_name))
            return False

    @property
    def full_name(self):
        """
        :return: Full name  of that person
        """
        return self.first_name + self.middle_name + self.last_name

    @full_name.setter
    def full_name(self, name):
        names = name.split()
        self.first_name = names[0]
        self.middle_name = " ".join(names[1:len(names) - 1])  # gets all the middle names
        self.last_name = names[-1]

    def get_user_email(self):
        # Return user email
        return '{}@gre.ac.uk'.format(self.email_name)

    def set_has_registered(self, has_registered):
        self.__has_registered = has_registered



class Candidate(Student):
    def __init__(self, name, login_id, pwd, has_registered=False, ):
        super().__init__(name=name, login_id=login_id, pwd=pwd)


class gsu_officers(Student):
    def __init__(self, petitionRunng):
        pass
