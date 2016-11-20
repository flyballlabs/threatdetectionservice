import database

# Connect to the database and provide a handle

db = database.connect()

class user_data(db.Model):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(45), unique=True)
    firstname = db.Column(db.String(45))
    lastname = db.Column(db.String(45))
    password = db.Column(db.String(45))
    email = db.Column(db.String(45), unique=True)
    company_id = db.Column(db.String(45))
    status = db.Column(db.String(45))
    lastlogin = db.Column(db.String(45))

    def __init__(self, user_id, username, firstname, lastname, password, email, company_id, status, lastlogin):
        self.user_id = user_id
        self.username = username
        self.firstname = firstname
        self.lastname = lastname
        self.password = password
        self.email = email
        self.company_id = company_id
        self.status = status
        self.lastlogin = lastlogin

    def __repr__(self):
        return '{user: %r}' % self.user_id


# class Post(db.Model):
#   id = db.Column(db.Integer, primary_key=True)
#   title = db.Column(db.String(128))
#   body = db.Column(db.Text)
#  
#   def __init__(self, title, body):
#         self.title = title
#         self.body = body
