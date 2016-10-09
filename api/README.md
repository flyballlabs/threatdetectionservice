# Threat Management Server API (Server API):
---

## Description
---

- This Server API provides a mechanism for threat management agents to obtain control information that specifies when and how data should be captured.  We assume that agents
are calling this API at least every 5 minutes.  This way we know that we can change the behavior of the agent within a 5 minute span.  
- The Threat Management Client scripts are in the /agent directory of this repo

## Functionality

The signature of the API, parameters and response are below

| URL | Request | Response |
| --- | ------- | -------- |
| /api/picontrollers/\<device\> | Where device is the name of the deployed agent | ``` json { start: \<start time\>, end: \<end time\>, cmd: \<command\> } ``` |

Setup
-----

- Install Python 3.0-3.5 and git.
- Run `setup.sh` (Linux, OS X, Cygwin) or `setup.bat` (Windows)
- Run `./rest-server.py to start the server (on Windows use `flask\Scripts\python rest-server.py` instead)
- Open `http://localhost:5000/index.html` on your web browser to run the client

