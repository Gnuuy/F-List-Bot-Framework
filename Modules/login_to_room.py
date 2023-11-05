from BotState import Bot

room_code = "adh-62e359721cbdac2218c3"
login_status = ""
HasHelpInfo = False
    
if room_code.strip() == "":
    raise NotImplementedError("You've not specified a room code for the bot to join. Remove this module if you do not want your bot to join a room.")

def handler(msg_pipe):
    msg = msg_pipe.get()
    
    Bot.send_out(Bot.Message(code="JCH", json={"channel": room_code}))
    Bot.send_out(Bot.Message(code="STA", json={"character": Bot.botname, "status":"online", "statusmsg":login_status}))
    
    
def predicate(msg):
    return msg.code == "IDN"
