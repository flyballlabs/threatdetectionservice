# Adding an API

We are using the Flask library to implement the RestFul interfaces for this project.  This library has an approach for implementing HTTP methods for an entity (eg. User, Agent, etc).  Their approach consist of using two classes to implement all of the HTTP methods needed to provide a robust API for an entity.  All API's in this project should follow this approach.  The procedure is described below.

## Add your resource definition to api/rest_server.py

The resource definition is just a mapping between the URI and the classes that will implement the logic for the API.

1. vi api/rest_server.py
2. find the section called `import endpoints`
3. add to the bottom `from <entity name>.endpoint import *`
4. add your resource configuration to the end of the file.  The resource configuration consists of your class names and the request URI.  In this example, we will be adding a RestFul API for the User entity.
```
api.add_resource(manageUser, '/api/user/<string:_username_>')
api.add_resource(manageUserList, '/api/user')
```
The manageUser class will contain functions to implement GET, DELETE and PUT HTTP methods for a single User entity.  The manageUserList will contains fucntions to implement GET and POST.  The GET in this case will return a list of users. The POST will add a new user.

## Make a model for your entity

The model contains a class representation of the underlying object in the database.  In most cases the entity will reside in the database, but it doesn't have to.

1. vi api/sql/models.py
2. Add your model.  The model for user is listed below as an example
```
3. Save your model

class user_data(db.Model):
    __tablename__ = 'user'
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8'  #latin1
    }

    user_id = db.Column(INTEGER, primary_key=True, unique=True, nullable=False)
    username = db.Column(VARCHAR(45), unique=True, nullable=False)
    firstname = db.Column(VARCHAR(45))
    lastname = db.Column(VARCHAR(45))      ##mysql dialect table format##
    password = db.Column(VARCHAR(45))      #Table('mytable', metadata,  #
    email = db.Column(VARCHAR(45))         #Column('data', String(32)), #
    company_id = db.Column(VARCHAR(45))    #mysql_engine='InnoDB',      #
    status = db.Column(VARCHAR(45))        #mysql_charset='utf8',       #
    lastlogin = db.Column(VARCHAR(45))     #mysql_key_block_size="1024")#
                                           ##############################
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
```

## Create the Logic for the API

1. `mkdir api/<entity name>`
2. `vi api/<entity name>/endpoint.py`
3. The format of the file based on a user entity is below
4. Save the file

```
from flask_restful import Resource, reqparse
from sql.models import *

class manageUser(Resource):
     @login_required
     def get(self,_username_):
        try:
        
        except Exception as e:
            return {'error': str(e)}
    @login_required
    def put(self,_username_):
        try:
        
        except Exception as e:
            return {'error': str(e)}
    @login_required
    def delete(self,_username_):
        try:
        
        except Exception as e:
            return {'error': str(e)}
            
class manageUserList(Resource):
     @login_required
     def get(self):
        try:
        
        except Exception as e:
            return {'error': str(e)}
            
    @login_required
    def post(self):
        try:
        
        except Exception as e:
            return {'error': str(e)}
  
  ```
  
Notice the @login_required statement.  This statement is called a function decoratar, which is used to force authentication before allowing the caller to access the endpoint.
  
## Test the API
  
 Use [Postman](http://www.getpostman.com) or Curl to test that the API has all of the following HTTP Verbs implemented:
 
manage`<entity name>`:

- GET (add a new entity)
- POST (get a list of entites)
 
manage`<entity name>`List:

- GET (for a particular entity id)
- DELETE (for a particular entity id)
- PUT  (for a particular entity id)

### Accesing the API Securely

You will need to make RestFul call to the /api/auth endpoint to receive an auth token, which will allow you to access the other endpoint.  The /api/auth endpoint allows the user to auth using HTTP Basic Authentication, which is insecure.  Therefore, in a production environment, you will need to use SSL to make the connection secure.  Below is an example of how this works:

```
curl -H "Accept: application/vnd.api+json" --user mack@goflyball.com:flyball -X GET 10.10.10.97:7777/api/auth
{
  "X-AUTH-TOKEN": "eyJhbGciOiJIUzI1NiIsImV4cCI6MTQ4MzMxMzk1NCwiaWF0IjoxNDgzMzEwMzU0fQ.eyJ1c2VyX2lkIjoxfQ.HAm5c7ILF4SGl37ibuunXrTdcmqQsYXx0O5epFgY4hE",
  "authentication": true,
  "message": "Authentication success"
}
```
<strong>Use the X-AUTH-TOKEN to make service call</strong>
```
curl -H "Accept: application/vnd.api+json" -H "X-AUTH-TOKEN: eyJhbGciOiJIUzI1NiIsImV4cCI6MTQ4MzMxMzk1NCwiaWF0IjoxNDgzMzEwMzU0fQ.eyJ1c2VyX2lkIjoxfQ.HAm5c7ILF4SGl37ibuunXrTdcmqQsYXx0O5epFgY4hE"  -X GET 10.10.10.97:7777/api/user
{"users": 
   [{"firstname": "Mack", "lastname": "Hendricks", "email": "mack@goflyball.com", "company_id": "1", "user_id": 1, "lastlogin": null, "active": 1, "username": "mack@goflyball.com"}, 
   {"firstname": "Tyler", "lastname": "Moore", "email": "tmoore@goflyball.com", "company_id": "1", "user_id": 2, "lastlogin": null, "active": 1, "username": "tmoore@goflyball.com"}], 
 "message": "User search success"}
```


# New GUI Page

The process of adding a new GUI page or adding additional functionality to an existing page:

1. Figure out the API components that you want to use.
2. Use [Postman](http://www.getpostman.com) or Curl to test that the API has the HTTP verbs implemented that you need.  For example, can you GET, POST and PATCH against the API.  If not, then fix the API or create a GITHUB Issue so that we can get the API fixed.
3. Copy the [GUI template page](gui/templates/gui.template) to the name of the file that you want to create.  For example, if you wanted to create a page for managing Agents then the name would be agents.html.
4. Copy the [GUI javascript template](gui/static/viewmodel.template) to <name of the gui page>viewmodel.js.  For example, the javasript file would be agentsviewmodel.js.  This javasript file contains the data-binding logic used to connect html elements to actions.  The data-binding logic is handled by [Knockout.js](http://knockout.js).

# Documentation
There should be a "README.md" for each top level directory in this project.  Any images used in the README.md files should be located in the ./guides/images folder.  Each README.md file should provide a brief overview of what's in that directory and it should direct the user to the [guides](./guides) directory, which will contain detailed documentation.
The images used for top level "README.md" files should be stored in the guide/images directory.  
