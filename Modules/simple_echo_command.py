from BotState import Bot

HasHelpInfo = True
command_name = "!echo"
command_description = "This command will make the bot return what you send it with a nice message included :D"

# Simple definition for an !echo command. The bot repeats what you said to it in private.
def handler(msg_pipe):
    msg = msg_pipe.get()
    
    if len(msg.json['message'][6:]) == 0:
        Bot.send_out(Bot.Message(code="PRI", json={"recipient": msg.json['character'], "message": "Hi there %s!\nI was expecting you to send text after the !echo command!\nCommand usage: !echo blah blah" % (msg.json['character'])}))
    else:
        Bot.send_out(Bot.Message(code="PRI", json={"recipient": msg.json['character'], "message": "Hi there %s!\nYou sent me: \"%s\"!" % (msg.json['character'], msg.json["message"][6:])}))
            
def predicate(msg):
    return msg.code == "PRI" and Bot.proper_command(msg.json["message"], "!echo")