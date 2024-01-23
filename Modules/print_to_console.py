from BotState import Bot

HasHelpInfo = False

def handler(msg_pipe):
        msg = msg_pipe.get()

        
        if msg.code == "JCH":
            print("[CHAT]: %s has joined \"%s\"" % (msg.json["character"], msg.json["title"]))
        else:
            print(f"[CHAT]: {msg}")

def predicate(msg):
        return msg.code not in ["STA", "NLN", "LIS", "CDS", "COL", "ICH", "FRL", "IGN", "FLN"]