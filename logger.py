import time


def printLog(msg, isError):
    now = time.strftime('%Y-%m-%d / %H:%M:%S')
    f = open("log.txt", "a")
    if isError:
        m = f"! [{now}] : {msg}\n"
    else:
        m = f"# [{now}] : {msg}\n"
    f.write(m)
