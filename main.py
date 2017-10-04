from __future__ import print_function

import os
import sys
import subprocess
import time

import pywintypes
from win32api import (
    GetCurrentProcess,
    OpenProcess,
    TerminateProcess,
)
from win32con import PROCESS_TERMINATE
from win32job import (
    AssignProcessToJobObject,
    CreateJobObject,
    JobObjectBasicProcessIdList,
    QueryInformationJobObject,
)

def parent():
    print("parent started", os.getpid())
    job = CreateJobObject(None, "my-first-job")
    AssignProcessToJobObject(job, GetCurrentProcess())
    for i in range(3):
        subprocess.Popen("python main.py /child")
    raw_input("press any key to kill all child processes:")
    try:
        job_processes = QueryInformationJobObject(None, JobObjectBasicProcessIdList)
        for pid in job_processes:
            if pid == os.getpid(): # Don't kill ourselves
                continue
            
            child_handle = OpenProcess(PROCESS_TERMINATE, True, pid)
            TerminateProcess(child_handle, 1)
            print("Killed", pid)
    except pywintypes.error:
        # Only here to demonstrate what exception is raised.
        raise

def child():
    print("child running", os.getpid())
    time.sleep(300)
    
if __name__ == '__main__':
    if "/child" in sys.argv:
        child()
    else:
        parent()
