import os
import datetime

def log(con, text):
    if os.path.exists("server_log.log") and os.path.isfile("server_log.log"):
        with open("server_log.log", "a") as f:
            f.write(f"""{datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")}:{con}:{text}\n""")
    else:
        with open("server_log.log", "w"):
            pass
        log(con, text)