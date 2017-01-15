#!/bin/bash

### install required modules / dependencies ###
sudo -i
cd /

# pcapy #
git clone https://github.com/CoreSecurity/pcapy.git
cd pcapy/
python setup.py install

# kafka-python #
cd /
pip install kafka-python
