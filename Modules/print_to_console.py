from BotState import Bot

HasHelpInfo = False

def handler(msg_pipe):
        msg = msg_pipe.get()
        
        print(f"[RAW CHAT MESSAGE]: {msg}")

# F-list is very noisy with things it sends. This logger is mostly intended just to log chat messages.
# If you want to log EVERYTHING the F-list server sends to you, then simply make this function return True
def predicate(msg):
        return msg.code not in ["STA", "NLN", "FLN", "LIS", "CDS", "COL", "ICH", "FRL", "IGN"]