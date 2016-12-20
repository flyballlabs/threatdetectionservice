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

# def connect():
# 
# engine = create_engine('mysql://tmp:tmp@127.0.0.1/tmp', convert_unicode=True)
# db = scoped_session(sessionmaker(autocommit=False,
#                                          autoflush=False,
#                                          bind=engine))
# Base = declarative_base()
# Base.query = db_session.query_property()
# 
# def init_db():
#     # import all modules here that might define models so that
#     # they will be registered properly on the metadata.  Otherwise
#     # you will have to import them first before calling init_db()
#     from sql.models import *
#     Base.metadata.create_all(bind=engine)