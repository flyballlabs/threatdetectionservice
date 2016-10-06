API:
=============

Description
-----------

- This API allows communication between a network tap (raspberry pi) and a host server.
- The scripts for capturing data on the network tap are all run locally on the client.
- The API therefore only needs to provide time synchronization and routing to additonal files.

Setup
-----

- Install Python 2.7 and git.
- Run `setup.sh` (Linux, OS X, Cygwin) or `setup.bat` (Windows)
- Run `./rest-server.py` to start the server (on Windows use `flask\Scripts\python rest-server.py` instead)
- Alternatively, run `./rest-server-v2.py` to start the Flask-RESTful version of the server.
- Open `http://localhost:5000/index.html` on your web browser to run the client

