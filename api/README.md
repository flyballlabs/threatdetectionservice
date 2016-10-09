# Threat Management Server API (Server API):

- This Server API provides a mechanism for threat management agents to obtain control information that specifies when and how data should be captured.  We assume that agents
are calling this API at least every 5 minutes.  This way we know that we can change the behavior of the agent within a 5 minute span.  
- The Threat Management Client scripts are in the /agent directory of this repo

## Functionality

The signature of the API, parameters and response are below

| URL | Request | Response |
| --- | ------- | -------- |
| /api/picontrollers/\<device\> | Where device is the name of the deployed agent | ``` { start: <start time>, end: <end time>, cmd: <command> } ``` |

### Response(s) Explained

This section contains detailed information on what the elements of the JSON response that's received from the API.

#### /api/picontrollers/\<device\>
---

- **start time:** Specifies when the agent should **start** capturing packet data 
- **end time:** Specifies when the agent should **stop** capturing packet data 
- **command:** A command will tell the agent which action to perform.  We only support the stop and end action as of right now.  A command overrides the start and end times.  For example, if the current time is 7am, the start time is 8am, but the client invokes the server API and gets an action of "start" then the agent will start capturing packet data immediately - even if it's before the start time 

Setup
-----

- Install Python 3.0-3.5 and git.
- Run `setup.sh` (Linux, OS X, Cygwin) or `setup.bat` (Windows)
- Run `./rest-server.py to start the server (on Windows use `flask\Scripts\python rest-server.py` instead)
- Open `http://<server ip address>:6668/index.html` on your web browser to run the client

