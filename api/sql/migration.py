''' #### migration example code ####
from app import app, db
from app.models import UsersPy
from flask import render_template, request, redirect, url_for, jsonify, session, flash

@app.route('/testdb/')
def testdb():
    admin = UsersPy('user1', 'password1')
    guest = UsersPy('user2', 'password2')

    db.session.add(admin)
    db.session.add(guest)

    #db.session.merge(admin)
    #db.session.merge(guest)
    db.session.commit()

    results = UsersPy.query.all()

    json_results = []
    for result in results:
      d = {'username': result.username,
           'password': result.password}
      json_results.append(d)

    return jsonify(items=json_results)
    

from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
from config import SQLALCHEMY_DATABASE_URI
from app import app, db
 
migrate = Migrate(app, db)
 
manager = Manager(app)
manager.add_command('db', MigrateCommand)
 
if __name__ == '__main__':
    manager.run()
'''
