# initializer for windows editable workspace

import traceback

def logw(msg, mode='a'):
    with open("msghost.log", mode) as logfile:
        logfile.write(f"{msg}\n\n")

try:
    from persepolis.scripts import persepolis
    persepolis.main()
except:
    logw(traceback.format_exc())
