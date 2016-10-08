'''
This program provides methods to
enable controlling rPi network tap
@author: devopsec
'''

import sys
sys.path.insert(0, ("/threatdetectionservice/agents/PiTap/"))
import rpi

class Controller(object):
    '''
    classdocs
    '''


    def __init__(self, params):
        '''
        Constructor
        '''
        
    #listen on port for api calls
    #conditionally execute modules
    
    apiInput = "someinput"
    
    if apiInput == "kafkaCapture":
        rpi.EnableCapture.enableCapture()
    elif apiInput == "disablecapture":
        rpi.DisableCapture.disableCapture()
    elif apiInput == "restartpi":
        rpi.RestartPi.restartPi()
    else:
        return print('something went wrong')
        