from app import create_app

app = create_app()

@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"