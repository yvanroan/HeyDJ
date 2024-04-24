#this is just a testpad for the app
# https://stackoverflow.com/questions/73012152/importerror-cannot-import-name-app-from-partially-initialized-module-market
# https://stackoverflow.com/questions/22711087/flask-importerror-no-module-named-app
# https://stackoverflow.com/questions/23340812/python-sqlite-table-a-has-no-column-named-x

from app import app
from app.routes import socketio
import os
    

if __name__ == "__main__":

    if os.getenv('use_ssl', 'false') == 'true':
        # SSL context for local development

        # context = ('localhost.pem', 'localhost-key.pem')  # You need to install mkcert to get these.
        socketio.run(app, certfile='localhost.pem', keyfile='localhost-key.pem', debug=True)
    else:
        # No SSL in production, Heroku handles SSL termination
        socketio.run(app, debug=True)
