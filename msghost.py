# msghost for windows editable installation.
# uncomment msghost.bat in script/browser_integration.py

import os
import sys
import struct
import traceback
from pathlib import Path
from io import BytesIO
from subprocess import Popen, PIPE
from subprocess import DETACHED_PROCESS
from subprocess import CREATE_NEW_PROCESS_GROUP
from subprocess import CREATE_BREAKAWAY_FROM_JOB

# these flags are needed to create a detached and independent child process in windows
# that can live after its parent dies.
creationflags = CREATE_BREAKAWAY_FROM_JOB | DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP

def logw(msg, mode='a'):
    with open("msghost.log", mode) as logfile:
        logfile.write(f"{msg}\n\n")

try:    
    raw_size = sys.stdin.buffer.read(4)  
    length = struct.unpack('@I', raw_size)[0]
    raw_data = sys.stdin.buffer.read(length)
    data = struct.pack(f"=I{length}s", length, raw_data)

    path = Path().joinpath("pdm.py")
    command = ["python", "-u", f"{path.resolve()}", "--nhm"]
    proc = Popen(command,
        stdin=PIPE, stderr=PIPE, stdout=PIPE, creationflags=creationflags)
    proc.communicate(input=data)
    sys.exit(0)

except Exception as e:
    logw(f"msghost.py error: {traceback.format_exc()}")
