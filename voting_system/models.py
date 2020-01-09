"""
class of student
Students eligible to vote are also stored on a simple text file called StudentVoters.txt. The contents of this file are
simply records, on separate lines, each containing the student user login ID and password name and separated by a
single space or comma.
"""


class login_management:
    def __init__(self):
        self.authenticated = False;
        self._login_id = None

    # https://flask-login.readthedocs.io/en/latest/#how-it-works Doc
    def is_active(self):
        """Returns True as all the users in text file is active"""
        return True

    def get_id(self):
        """Return the Student id- required by the module"""
        return self._login_id

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated

    def is_anonymous(self):
        """False, as anonymous Student aren't supported."""
        return False


class Student(login_management):
    def __init__(self, name, login_id, password, dob, faculty, directory_to_user_image=None, has_registered=False):
        self.first_name = name.split()[0]
        self.middle_name = " ".join(name.split()[1:len(name.split()) - 1])  # gets all the middle names
        self.last_name = name.split()[-1]
        self._login_id = login_id
        self._faculty = faculty
        self.email_name = self.first_name[
                              0] + self.last_name  # This property could be used to send out email after vote been casted
        self.__pwd = password
        self.dob = dob
        self.image = directory_to_user_image  # directory ref to user img
        self.__has_registered = has_registered

    # check if user is registered
    def is_registered(self):
        if self.__has_registered:
            print("The student %s %s has registered" % (self.first_name, self.last_name))
            return True
        else:
            print("The student %s %s has not registered" % (self.first_name, self.last_name))
            return False

    def get_user_id(self):
        # return users login id 
        return self._login_id

    @property
    def full_name(self):
        """
        :return: Full name  of that person
        """
        return " ".join([self.first_name, self.middle_name, self.last_name])

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

    def verify_password(self, password):
        """
        To verify the users password
        :param password:
        :return:
        """
        if self.__pwd == password:
            return True
        else:
            return False

    def get_user_faculty(self):
        """
        :return:Returns users faculty
        """
        return self._faculty

    def __eq__(self, other):
        """
        Check weather the other object with similar attributes
        """
        if not isinstance(other, Student):
            return NotImplemented
        return (self.full_name.lower(), self._login_id, self.dob) == (other.full_name.lower(), other._login_id, other.dob)

    def __hash__(self):
        """
        Returns hash for this object
        """
        return hash((self.full_name, self._login_id, self.dob))


    def get_user_ppi_info(self):
        """
        Returns user's Full name, dob and loginid
        """
        return (self.first_name, self.dob, self._login_id, self._faculty)


class Candidate(Student):
    def __init__(self, name, login_id, password, dob, faculty, position, logoref=None, campaign=None, promises=None,
                 has_registered=False):
        super().__init__(name, login_id, password, dob, faculty, has_registered)
        self.position = position
        self.campaign_name = campaign  # candidates campaigning name
        self.campaign_promises = promises
        self.logo = logoref

    def get_user_ppi_info(self):
        """
        Returns user's Full name, dob and loginid
        """
        return (self.first_name, self.dob, self._login_id, self._faculty, self.position)

class gsu_officers(Student):
    def __init__(self, petitionRunng):
        pass
