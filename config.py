from dotenv import load_dotenv
import os

load_dotenv()

db_user = os.environ.get('DB_USER')
db_password = os.environ.get('DB_PASSWORD')
db_uri = os.environ.get('DB_URI')
db_name_production = os.environ.get('DB_NAME_PRODUCTION')
db_name_testing = os.environ.get('DB_NAME_TESTING')
db_port = os.environ.get('DB_PORT')


class Config():
    pass


class DevelopmentConfig(Config):
    """Class for storing information about development database
    Attributes:
        DEBUG: a boolean indicates the debug mode is activated or not
        SQLALCHEMI_DATABASE_URI: a string that contain information about uri to access development database
    """
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(
        db_user, db_password, db_uri,db_port, db_name_production)


class TestingConfig(Config):
    """Class for storing information about testing database
    Attributes:
        TESTING: a boolean indicates the testing mode is activated or not
        SQLALCHEMI_DATABASE_URI: a string that contain information about uri to access testing database
    """
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(
        db_user, db_password, db_uri,db_port, db_name_testing)
