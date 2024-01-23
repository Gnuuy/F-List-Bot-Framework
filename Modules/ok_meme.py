from BotState import Bot

HasHelpInfo = False

def handler(msg_pipe):
        msg = msg_pipe.get()
        Bot.send_out(Bot.Message(code="MSG", json={"channel": msg.json["channel"], "message": "[eicon]oke[/eicon]"}))
    
def predicate(msg):
    return msg.code == "MSG" and ((((msg.json["message"].startswith("bot ") and " stupid " in msg.json["message"]) or (" bot " in msg.json["message"] and " stupid " in msg.json["message"])) or ((msg.json["message"].startswith("bot ") and " stupid" in msg.json["message"]) or (" bot " in msg.json["message"] and " stupid" in msg.json["message"]))) or (((msg.json["message"].startswith("bot ") and " dumb " in msg.json["message"]) or (" bot " in msg.json["message"] and " dumb " in msg.json["message"])) or ((msg.json["message"].startswith("bot ") and " dumb" in msg.json["message"]) or (" bot " in msg.json["message"] and " dumb" in msg.json["message"]))))