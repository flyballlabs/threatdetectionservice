# Threat Detection Service

We are focused on delievering a Threat Detection Service for Detroit Schools and Detroit Neighborhoods, but the platform could be used for different purposes.  

We are focused on schools because they need to have efficent networks with the increased use of online testing.  We believe that a large portion of the schools bandwidth is being utilzied by hackers trying to take control of machines on the network to commit cyberattacks against others.  Also, there are computer viruses that install as ransomware where they pose as legitimate anti-virus software, but really they are just trying to obtain credit card numbers by having the user purchase fake virus software.  Lastly, we want to protect the identity of the students and prevent unauthorizied access to their private information, which could be used to hijack the identity of the student.

In Detroit neighborhoods we are not focused on detecting cyberattacks, but we are focused on detecting suspensious behaviour that may threaten the safty of Detroit residents.

Our Threat Detection Service is using [Apache Metron](http://metron.incubator.apache.org/) as the core engine.  For Detroit neighborhoods we will use the facial recognition software provided by [Kairos](https://www.kairos.com/)

## Repo Structure

agents - Contains the software for the agents that are deployed at the Detroit Schools. The agents are deployed on [Raspberry Pi Model 3](https://www.raspberrypi.org/products/raspberry-pi-3-model-b/)



# Installation Documentation
This install documentation is for ubuntu 16.04

## Installing uwsgi

Installing the dependencies and compiling uwsgi.

```
apt install build-essential python-dev
wget http://projects.unbit.it/downloads/uwsgi-latest.tar.gz
tar -xzf uwsgi-latest.tar.gz
cd uwsgi-2.0.14/
make
```


Create a simple test python script

```
vim foobar.py
```

```
def application(env, start_response):
        start_response('200 OK', [('Content-Type','text/html')])
        return [b"Hello World"]
```

Now run this test script with uwsgi

```
./uwsgi --http :6665 --wsgi-file foobar.py
```


You can now browse to 10.10.10.154:6668 and you should se hello world printed. 


## Installing fetask
apt-get install python-pip python3-pip
/usr/bin/pip3 install Flask

```
vim myflaskapp.py
```

```
#!/usr/bin/python3
from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return "<span style='color:red'>I am app 1</span>"
```

Now run the flask test app

```
./uwsgi --http :6668 --wsgi-file myflaskapp.py --callable app --processes 4 --threads 2
```

You can now browse to `<ip>:6668` to confirm flask is working. 

It should say 

```
I am app 1
```






## notes

capturing is happening on port 6667

port 6668 is the control port
	pi is periodically calling the ubuntu server on this port for configuration.
	pi also receives commands on this port

can't rely on port forwarding to get access to the pi, so pi needs to call out to this server on a public ip. 
		 
		
		
## Install setup.sh
Run setup.sh, this will install the python dependencies via pip. The depencies are listed `requirements.txt` 


## Install the python application

###This next secction needs some work, setup.sh is not setup yet. 
###We currently need to point to the python3 and pip3 binaries, in /usr/bin/python3 and /usr/bin/pip3
run `setup.sh`, which will install all the dependencies and setup the virtual environment.


apt-get install python3-venv
apt-get install python3-virtualenv
python3 -m venv flask


I created a requirements.txt with the following

 flask
 flask-login
 flask-openid
 flask-mail
 flask-sqlalchemy
 sqlalchemy-migrate
 flask-whooshalchemy
 flask-wtf
 flask-babel
 guess_language
 flipflop
 coverage
itsdangerous
Werkzeug
Jinja2


We ran into some problems getting the virtualenv.py script to run, not sure if we actually need this. 

/usr/bin/python3 virtualenv.py flask


We are able to run the script with just python, and I assume it is using some python http server instead of uwsgi.

/usr/bin/python3 rest-server.py


When running with uwsgi, we get the following. 

root@devbox /usr/local/src/threatdetectionservice/api # /usr/local/src/uwsgi-2.0.14/uwsgi --http-socket 0.0.0.0:6668 -wsgi-file rest-server.py --callable app --processes 4 --threads 2
unable to load configuration from rest-server.py


## To run the rest-server without uswgi, run the following from /usr/local/src/threatdetectionservice/api
/usr/bin/python3 rest-server.py
