from BotState import Bot

HasHelpInfo = True
command_name = "!help"
command_description = ""

def handler(msg_pipe):
    msg = msg_pipe.get()
    
    cmds = []
    for item in Bot.dispatcher.threadpool:
        if item.isPublicFacingCommand:
            cmds.append(item.cmdname)
    
    json = {"message": "Currently loaded commands: [ %s ]" % ", ".join(cmds)}
    
    if msg.code == "PRI":
        json["recipient"] = msg.json["character"]
    else:
        json["channel"] = msg.json["channel"]
        
    Bot.send_out(Bot.Message(code=msg.code, json=json))
    
    
def predicate(msg):
    return (msg.code == "MSG" or msg.code == "PRI") and Bot.proper_command(msg.json["message"], "!help")