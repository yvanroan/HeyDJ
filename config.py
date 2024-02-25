import os
# from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
# load_dotenv(os.path.join(basedir, '.env'))

class Config(object):
    # I'm taking the database URL from the DATABASE_URL environment variable, 
    # and if that isn't defined, I'm configuring a database named app.db located in the main directory of the application, 
    # which is stored in the basedir variable.
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db') # or os.environ.get('DATABASE_URL')
