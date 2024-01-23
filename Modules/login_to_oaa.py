from BotState import Bot
from BotSingleton import BotSingleton

bot_instance = BotSingleton()
room_code = bot_instance.room
login_status = """
[session=Oral Addicts Anonymous]adh-62e359721cbdac2218c3[/session]
Type !help to me for commands!

Try our new gloryhole system! PM me !intro for an introduction!"""
HasHelpInfo = False
    
if room_code.strip() == "":
    raise NotImplementedError("You've not specified a room code for the bot to join. Remove this module if you do not want your bot to join a room.")

def handler(msg_pipe):
    msg = msg_pipe.get()
    
    Bot.send_out(Bot.Message(code="JCH", json={"channel": room_code}))
    Bot.send_out(Bot.Message(code="STA", json={"character": Bot.botname, "status":"online", "statusmsg":login_status}))
    
    
def predicate(msg):
    return msg.code == "IDN"
