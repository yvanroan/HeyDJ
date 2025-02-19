import os
from dotenv import load_dotenv

load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    # I'm taking the database URL from the DATABASE_URL environment variable, 
    # and if that isn't defined, I'm configuring a database named app.db located in the main directory of the application
    
    DATABASE_URL = os.environ.get('HEROKU_POSTGRESQL_GRAY_URL', f'sqlite:///{os.path.join(basedir, "app.db")}')
    

    # DATABASE_URL=f'sqlite:///{os.path.join(basedir, "app.db")}'
    
    if DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
            
    print(DATABASE_URL)
    SQLALCHEMY_DATABASE_URI = DATABASE_URL
