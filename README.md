# Threat Detection Service

We are focused on delievering a Threat Detection Service for Detroit Schools and Detroit Neighborhoods, but the platform could be used for different purposes.  

We are focused on schools because they need to have efficent networks with the increased use of online testing.  We believe that a large portion of the schools bandwidth is being utilzied by hackers trying to take control of machines on the network to commit cyberattacks against others.  Also, there are computer viruses that install as ransomware where they pose as legitimate anti-virus software, but really they are just trying to obtain credit card numbers by having the user purchase fake virus software.  Lastly, we want to protect the identity of the students and prevent unauthorizied access to their private information, which could be used to hijack the identity of the student.

In Detroit neighborhoods we are not focused on detecting cyberattacks, but we are focused on detecting suspensious behaviour that may threaten the safty of Detroit residents.

Our Threat Detection Service is using [Apache Metron](http://metron.incubator.apache.org/) as the core engine.  For Detroit neighborhoods we will use the facial recognition software provided by [Kairos](https://www.kairos.com/)

## Repo Structure

agents - Contains the software for the agents that are deployed at the Detroit Schools. The agents are deployed on [Raspberry Pi Model 3](https://www.raspberrypi.org/products/raspberry-pi-3-model-b/)



# Installation Documentation

## Installing uwsgi
apt install build-essential python-dev
wget http://projects.unbit.it/downloads/uwsgi-latest.tar.gz
tar -xzf uwsgi-latest.tar.gz
cd uwsgi-2.0.14/
make



vim foobar.py

```
def application(env, start_response):
        start_response('200 OK', [('Content-Type','text/html')])
        return [b"Hello World"]
```

./uwsgi --http :9090 --wsgi-file foobar.py


You can now browse to 10.10.10.154:9090 and you should se hello world printed. 


## Installing flask
apt-get install python-pip python3-pip
/usr/bin/pip3 install Flask


vim myflaskapp.py
```
#!/usr/bin/python3
from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return "<span style='color:red'>I am app 1</span>"
```

./uwsgi --http :9090 --wsgi-file myflaskapp.py --callable app --processes 4 --threads 2

You can now browse to <ip>:9090 to confirm flask is working. 

It should say 
I am app 1
