class NotValidData(Exception):
    """Exception raised for errors if data in csv file is not valid or empty

        expression -- input expression in which the error occurred
        message -- explanation of the error
    """

    def __init__(self, expression, message):
        self.expression = expression
        self.message = message


class ConfigError(Exception):
    """Exception raised for errors if data in csv file is not valid or empty

        expression -- input expression in which the error occurred
        message -- explanation of the error
    """

    def __init__(self, expression, message):
        self.expression = expression
        self.message = message
