from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy import create_engine
# from sqlalchemy.orm import scoped_session, sessionmaker
# from sqlalchemy.ext.declarative import declarative_base

app = Flask('rest_server')
app.config.setdefault('SQLALCHEMY_DATABASE_URI', 'mysql://tmp:tmp@127.0.0.1/tmp')
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

def connect():

    db = SQLAlchemy(app)
    return db
