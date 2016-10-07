'''
This program provides methods to
enable controlling rPi network tap
@author: devopsec
'''

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
    
    if apiInput == "enablecapture":
        rpi.EnableCapture.enableCapture()
    elif apiInput == "disablecapture":
        rpi.DisableCapture.disableCapture()
    elif apiInput == "restartpi":
        rpi.RestartPi.restartPi()
    else:
        