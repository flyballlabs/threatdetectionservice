from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask('rest_server')
app.config.setdefault('SQLALCHEMY_DATABASE_URI', 'mysql://tmp:tmp@127.0.0.1/tmp')

def connect():

    db = SQLAlchemy(app)
    return db
