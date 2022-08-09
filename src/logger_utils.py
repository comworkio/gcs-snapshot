import os

from datetime import datetime

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def log_msg (log_level, message):
    current_date = datetime.now()
    cong_log_level = os.environ['LOG_LEVEL']
    if log_level == "error" or log_level == "ERROR" or log_level == "fatal" or log_level == "FATAL":
        eprint ("[{}][{}] {}".format(current_date.isoformat(), log_level, message))
    elif cong_log_level == log_level or cong_log_level == "debug" or cong_log_level == "DEBUG":
        print ("[{}][{}] {}".format(current_date.isoformat(), log_level, message))
