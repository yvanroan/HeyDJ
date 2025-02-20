#this is just a testpad for the app
# https://stackoverflow.com/questions/73012152/importerror-cannot-import-name-app-from-partially-initialized-module-market
# https://stackoverflow.com/questions/22711087/flask-importerror-no-module-named-app
# https://stackoverflow.com/questions/23340812/python-sqlite-table-a-has-no-column-named-x

from app import app
from app.routes import socketio
from dotenv import load_dotenv
import os
import ssl

load_dotenv()

if __name__ == "__main__":

    if os.getenv('use_ssl', 'false') == 'true':
        # SSL context for local development
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.load_cert_chain('localhost.pem', 'localhost-key.pem')  # You need to install mkcert to get these.
        socketio.run(
            app,
            ssl_context=context, 
            debug=True,
            use_reloader=False
        )
    else:
        socketio.run(app, debug=False)

