'''
@Summary: Utility Methods for dynamic actions during program operation.
@Author: devopsec
'''

import os, sys, socket, inspect

def getWorkingDirs():
    ''' Returns project dir, parent dir, and current dir of calling script as dict'''

    project_dir, parent_dir, current_dir = None
    if os.path.exists(os.path.dirname(__file__)):
        current_dir = os.path.abspath(os.path.dirname(__file__))
        parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

    else:
        current_dir = os.path.abspath(os.getcwd())
        parent_dir = os.path.abspath(os.path.join(os.getcwd(), '..'))

    check = os.path.exists(parent_dir)
    while (check != False):
        project_dir = os.getcwd()
        os.chdir("..")
        check = os.path.exists(os.path.join(os.getcwd(), '..'))

    return {
        'project_dir' : project_dir,
        'parent_dir' : parent_dir,
        'current_dir' : current_dir
    }

def setProjectPath(dir=None):
    ''' Sets project path to current calling script location or provided dir and move to it '''

    if not dir == None and os.path.exists(dir):
        proj_path = os.path.abspath(dir)
        os.chdir(proj_path)
        sys.path.append(proj_path)
        print("Project path set to: " + proj_path)
    else:
        if os.path.exists(os.path.dirname(__file__)):
            proj_path = os.path.abspath(os.path.dirname(__file__))
            os.chdir(proj_path)
            sys.path.append(proj_path)

        else:
            proj_path = os.path.abspath(os.getcwd())
            os.chdir(proj_path)
            sys.path.append(proj_path)

def get_current_ip():
    ''' Returns current ip of system '''

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]

def get_hostname():
    ''' Returns hostname of current host '''

    if socket.gethostname().find('.') >= 0:
        return socket.gethostname()
    else:
        return socket.gethostbyaddr(socket.gethostname())[0]

def script_info():
    '''
    Returns a dictionary with information about the running top level Python
    ---------------------------------------------------------------------------
    dir:    directory containing script or compiled executable
    name:   name of script or executable
    source: name of source code file
    ---------------------------------------------------------------------------
    "name" and "source" are identical if and only if running interpreted code.
    When running code compiled by py2exe or cx_freeze, "source" contains
    the name of the originating Python script.
    If compiled by PyInstaller, "source" contains no meaningful information.
    '''

    #---------------------------------------------------------------------------#
    #         scan through call stack for caller information                    #
    #---------------------------------------------------------------------------#
    for teil in inspect.stack():
        # skip system calls
        if teil[1].startswith("<"):
            continue
        if teil[1].upper().startswith(sys.exec_prefix.upper()):
            continue
        trc = teil[1]

    # trc contains highest level calling script name, check if we have been compiled
    if getattr(sys, 'frozen', False):
        scriptdir, scriptname = os.path.split(sys.executable)
        return {
            "dir" : scriptdir,
            "name" : scriptname,
            "source" : trc
        }

    # from here on, we are in the interpreted case
    scriptdir, trc = os.path.split(trc)
    # if trc did not contain directory information,
    # the current working directory is what we need
    if not scriptdir:
        scriptdir = os.getcwd()

    scr_dict = {
        "name" : trc,
        "source" : trc,
        "dir" : scriptdir
    }
    return scr_dict