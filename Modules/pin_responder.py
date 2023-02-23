from BotState import Bot

# Responds to F-list's ping messages that come in to make sure you're alive.
# You shouldn't change this.
HasHelpInfo = False

def handler(msg_pipe):
    msg_pipe.get()
    Bot.send_out(Bot.Message(code="PIN"))
    
def predicate(msg):
    return msg.code == "PIN"