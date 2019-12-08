from datetime import datetime

#SET START and END date of voting
# Needs to be  in dd/mm/yyyy format
V_START_DATE = "28/11/2019 09:00:00"
# Needs to be  in dd/mm/yyyy format
V_END_DATE = "28/11/2019 09:00:00"

def parse_datetime(dt_string):
    """
    parses the dt in dd/mm/yyyy format
    :param dt_string:
    :return: parsed dt
    """
    return datetime.strptime(dt_string, "%d/%m/%Y %H:%M:%S")

class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY='\x88\xbf\xaa[\xa9\xc6\x8f\x8c x\x9bV\xe1C\x0e\n\xe9\x1c`\xc0\xa3\xd8\xcd\xc3' #to keep client sides ewcure 
    VOTING_START_DATE = parse_datetime(V_START_DATE)
    VOTING_END_DATE = parse_datetime(V_END_DATE)

class ProductionConfig(Config):
    # same as the base class
    pass


class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = True


