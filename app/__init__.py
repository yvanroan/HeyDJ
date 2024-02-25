from flask import Flask
import time
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()


def create_app(config_class=Config):

    app = Flask(__name__)
    app.config.from_object(config_class)
    print("yo")
    # with app.app_context():
    #     db.drop_all()
    #if you need to erase the whole db
    db.init_app(app)
    migrate.init_app(app, db)
    time.sleep(2)
    print("App has being initialized")
    return app



# the db object that represents the database. Then I added migrate, to represent the database migration engine. 
#I'm importing a new module called models at the bottom. This module will define the structure of the database.

# from app.views import viewBp
# app.register_blueprint(viewBp)

from app import routes, models
