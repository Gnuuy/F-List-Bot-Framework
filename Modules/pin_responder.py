from BotState import Bot

HasHelpInfo = False

def handler(msg_pipe):
    msg_pipe.get()
    Bot.send_out(Bot.Message(code="PIN"))
    
def predicate(msg):
    return msg.code == "PIN"