'''
This script restarts OS
on rPi network tap
@author: devopsec
'''

def restartPi():
    
    from time import sleep
    
    #may need to install psutil on host
    import subprocess, os, sys
    
    subprocess.run("signal.SIGINT", shell=True)
    subprocess.run("killall -u anon", shell=True)
    subprocess.run("shutdown -r 0", shell=True)
    
    try:
        import psutil
        def kill(p_pid):
            process = psutil.Process(p_pid)
            for proc in process.get_children(recursive=True):
                proc.kill()
                process.kill()
    except:
        pass
    
    p = subprocess.Popen(['gnome-terminal -e bash'], shell=True)
    try:
        p.wait(timeout=3)
    except p.TimeoutExpired:
        kill(p.pid)
        
    try:
        sys.exit(0)
        sleep(5)
    except:
        os._exit(0)
