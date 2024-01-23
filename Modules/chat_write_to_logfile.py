from BotState import Bot
import datetime
import pathlib

HasHelpInfo = False

def handler(msg_pipe):
    msg = msg_pipe.get()
    logdir = pathlib.Path(pathlib.Path.cwd() / "logs")
    if not logdir.exists():
        logdir.mkdir(exist_ok=True)
        
    filename = msg.json["channel"] if "channel" in msg.json.keys() else msg.json["character"]
           
    open("logs/%s.log" % filename, "a", encoding="utf-8").write("[%s] %s: %s\n" % (str(datetime.datetime.now()), msg.json["character"], msg.json["message"]))
    
def predicate(msg):
    return msg.code == "MSG" or msg.code == "PRI"