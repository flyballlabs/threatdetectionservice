
'''
#### sample code ####
from app import app, db

class user(db.Model):

  __tablename__ = "userspy"

  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String, nullable=False)
  password = db.Column(db.String, nullable=False)

  def __init__(self, username, password):
    self.username = username
    self.password = password

  def __repr__(self):
    return '<title {}'.format(self.username)
    
    from app import db
class Post(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(128))
  body = db.Column(db.Text)
 
  def __init__(self, title, body):
        self.title = title
        self.body = body
'''