from BotState import Bot
import datetime
import pathlib

HasHelpInfo = False

def handler(msg_pipe):
    msg = msg_pipe.get()
    logdir = pathlib.Path(pathlib.Path.cwd() / "room_logs")
    if not logdir.exists():
        logdir.mkdir(exist_ok=True)
           
    open("room_logs/%s.log" % msg.json["channel"], "a", encoding="utf-8").write("[%s] %s: %s\n" % (str(datetime.datetime.now()), msg.json["character"], msg.json["message"]))
    
def predicate(msg):
    return msg.code == "MSG"