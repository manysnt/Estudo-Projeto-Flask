import flask
from app import app

app = flask(__name__)

if __name__ == '__main__':
    app.run(debug=True) 

