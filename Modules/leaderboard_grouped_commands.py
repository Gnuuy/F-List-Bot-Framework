from BotState import Bot
import pathlib
import json as jsonlib

HasHelpInfo = True
command_name = "!leaderboard, !tokens, !complete_leaderboard, !archived_leaderboards"
command_description = ""
    
def getTop3():
    leaderboard = jsonlib.loads(open("leaderboard.txt", "r").read())
    top3 = sorted(list(leaderboard.items()), key= lambda x: x[1], reverse=True)[:3]
    output = ""
    
    for item in top3:
        output += "[user]%s[/user], with %s tokens.\n" % (item[0], item[1])
        
    return output
    
def getLeaderboard(boardfile=str(pathlib.Path("leaderboard.txt").resolve())):
    print(boardfile)
    return jsonlib.loads(open(boardfile, "r").read())
    
def getWholeLeaderboardText(boardfile):
    board = getLeaderboard(boardfile)
    top = sorted(list(board.items()), key= lambda x: x[1], reverse=True)
    output = ""
    
    for item in top:
        output += "[user]%s[/user], with %s tokens.\n" % (item[0], item[1])
    return output

def handler(msg_pipe):
    msg = msg_pipe.get()
    
    if msg.json['message'].startswith("!leaderboard"):
        if msg.code == "MSG":
            Bot.send_out(Bot.Message(code="MSG", json={"channel": msg.json["channel"], "message": "Hey there %s! The top 3 of the leaderboard are below. Say \"!complete_leaderboard\" to me privately if you'd like the entire thing in your PMs!\n%s" % (msg.json["character"], getTop3())}))
        elif msg.code == "PRI":
            Bot.send_out(Bot.Message(code="PRI", json={"recipient": msg.json["character"], "message": "Hiya %s, here's the leaderboard, just for you:\n\n%s" % (msg.json["character"], getWholeLeaderboardText("leaderboard.txt"))}))
    elif msg.json['message'].startswith("!complete_leaderboard"):
        if msg.code == "MSG":
            Bot.send_out(Bot.Message(code="MSG", json={"channel": msg.json["channel"], "message": "I'll send you the whole leaderboard privately. Check your PMs!"}))
        Bot.send_out(Bot.Message(code="PRI", json={"recipient": msg.json["character"], "message": "Hiya %s, here's the leaderboard, just for you:\n\n%s" % (msg.json["character"], getWholeLeaderboardText("leaderboard.txt"))}))
    elif msg.json['message'].startswith("!archived_leaderboards"):
        Bot.send_out(Bot.Message(code="PRI", json={"recipient": msg.json["character"], "message": "Hiya %s, here's the archived leaderboards, just for you:\n\n[b][b]2023's Leaderboard:[/b][/b]\n%s\n\n[b][b]2022's Leaderboard:[/b][/b]\n%s\n\n[b][b]2021's Leaderboard:[/b][/b]\n%s" % (msg.json["character"], getWholeLeaderboardText("2023board.txt"), getWholeLeaderboardText("2022board.txt"), getWholeLeaderboardText("2021board.txt"))}))
        
    elif msg.json['message'].startswith("!tokens"):
        # Asking for their own tokens?
        if len(msg.json['message']) <= len("!tokens "):
            board = getLeaderboard()
            name = msg.json["character"]
            if name.lower() in map(lambda x: x.lower(), board.keys()):
                if msg.code=="MSG":
                    Bot.send_out(Bot.Message(code="MSG", json={"channel": msg.json["channel"], "message": "[user]%s[/user], You've got %s %s." % (msg.json["character"], getLeaderboard()[msg.json["character"].lower()], "tokens" if getLeaderboard()[msg.json["character"].lower()] != 1 else "token")}))
                if msg.code=="PRI":
                    Bot.send_out(Bot.Message(code="PRI", json={"recipient": msg.json["character"], "message": "[user]%s[/user], You've got %s %s." % (msg.json["character"], getLeaderboard()[msg.json["character"].lower()], "tokens" if getLeaderboard()[msg.json["character"].lower()] != 1 else "token")}))
            else:
                if msg.code=="MSG":
                    Bot.send_out(Bot.Message(code="MSG", json={"channel": msg.json["channel"], "message": "Sorry friend, I'm not seeing any tokens recorded for your name in my database."}))
                if msg.code=="PRI":
                    Bot.send_out(Bot.Message(code="PRI", json={"recipient": msg.json["character"], "message": "Sorry friend, I'm not seeing any tokens recorded for your name in my database."}))
                
def predicate(msg):
    if msg.code == "MSG" or msg.code == "PRI":
        if Bot.proper_command(msg.json["message"], "!leaderboard"):
            return True
        if Bot.proper_command(msg.json["message"], "!complete_leaderboard"):
            return True
        if Bot.proper_command(msg.json["message"], "!tokens"):
            return True
        if Bot.proper_command(msg.json["message"], "!archived_leaderboards"):
            return True
    return False
