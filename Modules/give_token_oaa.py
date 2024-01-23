from BotState import Bot
import json as jsonlib
import requests
import pathlib

HasHelpInfo = True
command_name = "!give_token"
command_description = ""

def getLeaderboard(boardfile=str(pathlib.Path("leaderboard.txt").resolve())):
    print(boardfile)
    return jsonlib.loads(open(boardfile, "r").read())

def handler(msg_pipe):
        msg = msg_pipe.get()
        
        thesplit = msg.json["message"].split(" ")
        msgparams = (thesplit[0], " ".join(thesplit[1:-1]), thesplit[-1])
        mods = ["Moo", "Keyah","Kemonomimi GM", "Captain Eberswalde", "Mayhem Maid", "Fetch me their souls", "Cassandra Star", "Fellation", "Prolific", "Leuna Madra", "Clari", "Brenda", "Petulant", "Kemonomimi Hub", "Sarathiel", "Nine Lives", "Red Shadowscale", "Ellis Ailven", "Red Eyed Bunny", "ElpheIt Valentine"]

        if msg.json["character"].lower() not in map(lambda x: x.lower(), mods):
            Bot.send_out(Bot.Message(code="MSG", json={"channel": msg.json["channel"], "message": "You absolute silly billy. You don't look like a moderator to me! Why are you trying to run this command?!"}))
            return
        print("CHECKPOINT 2")
        if msg.json["character"].lower() in map(lambda x: x.lower(), mods):
            if len(msgparams) != 3:
                Bot.send_out(Bot.Message(code="MSG", json={"channel": msg.json["channel"], "message": "Incorrect command syntax.\nUsage: !give_token <Character Name:String> <amount:Integer>"}))
            else:
                try:
                    amount = int(msgparams[2])
                except:
                    Bot.send_out(Bot.Message(code="MSG", json={"channel": msg.json["channel"], "message": "Sorry boss, that second thing there doesn't look like an integer to me... Please try again!\nIncorrect command syntax.\nUsage: !give_token <Character Name:String> <amount:Integer>"}))
                    return
                
                othername = msgparams[1]
                print("CHECKPOINT 3")
                if len(othername) > 20:
                    Bot.send_out(Bot.Message(code="MSG", json={"channel": msg.json["channel"], "message": "That name looks kinda longer than any character name on the site. I'm not gonna look for that."}))
                    return
                print("CHECKPOINT 4")
                request_data = {"account": Bot.username, "ticket": Bot.getTicket(), "name":othername}
                
                rsponse = requests.post('https://www.f-list.net/json/api/character-data.php', data=request_data)
                if rsponse.json()["error"] == "Character not found.":
                    Bot.send_out(Bot.Message(code="MSG", json={"channel": msg.json["channel"], "message": "Hmm... my sources tell me that \"%s\" isn't actually a character on the site. Did you make a typo?" % othername}))
                    return
                elif rsponse.json()["error"] != "":
                    Bot.send_out(Bot.Message(code="MSG", json={"channel": msg.json["channel"], "message": "I couldn't check if that's actually a username. Is it perhaps that you've included invalid characters or some sort of broken name?"}))
                    return
                
                print("CHECKPOINT 6")
                board = getLeaderboard()
                if board == {}:
                    raise Exception("I tried to fetch board state and it seemed bad. Help, papa!")
                print("CHECKPOINT 7")
                if othername.lower() == msg.json["character"].lower() and msg.json["character"].lower() != "moo":
                    Bot.send_out(Bot.Message(code="MSG", json={"channel": msg.json["channel"], "message": "You are not allowed to give yourself tokens."}))
                    return
                        
                if othername.lower() == "moo" and msg.json["character"] != "Moo":
                    Bot.send_out(Bot.Message(code="MSG", json={"channel": msg.json["channel"], "message": "You may not give Moo tokens. The Owner does not participate in token shenanigans."}))
                    return
                print("CHECKPOINT 8")
                if othername.lower() not in map(lambda x: x.lower(), board.keys()):
                    board[othername.lower()] = 0
                        
                if (amount > 15 or amount < -15) and msg.json["character"] == "Moo":
                    Bot.send_out(Bot.Message(code="MSG", json={"channel": msg.json["channel"], "message": "Hmm... looks like you ran this command correctly, but that is a [b]lot[/b] of tokens homie. Consult Moo please... wait- [eicon]wj huh[/eicon] the fuck?! You are Moo! You should bloody know better. [eicon]newsbap[/eicon]"}))
                    open("tokenlog.txt", "a").write("WARNING, %s ATTEMPTED TO GIVE %d TOKENS TO %s\n--------------------------------\n" % (msg.json["character"], amount, othername))
                    return
                        

                print("CHECKPOINT 9")
                if amount > 15 or amount < -15:
                    if amount == 69:
                        Bot.send_out(Bot.Message(code="MSG", json={"channel": msg.json["channel"], "message": "Nice."}))
                    Bot.send_out(Bot.Message(code="MSG", json={"channel": msg.json["channel"], "message": "Hmm... looks like you ran this command correctly, but that is a [b]lot[/b] of tokens homie. Consult Moo please."}))
                    open("tokenlog.txt", "a").write("WARNING, %s ATTEMPTED TO GIVE %d TOKENS TO %s\n--------------------------------\n" % (msg.json["character"], amount, othername))
                    return
                        
                print("CHECKPOINT 10")
                board[othername.lower()] += amount
                    
                open("tokenlog.txt", "a").write("[USER]: %s Has updated the token leaderboard.\n[UPDATE]:%s [%s]\n--------------------------------\n" % (msg.json["character"], othername, amount))
                open("leaderboard.txt", "w").write(jsonlib.dumps(board))
                print("CHECKPOINT 11")
                Bot.send_out(Bot.Message(code="MSG", json={"channel": msg.json["channel"], "message": "[user]%s[/user] Now has %s %s tokens on the leaderboard." % (othername, str(amount if amount > 0 else amount * -1), "less" if amount < 0 else "more")}))
def predicate(msg):
        return msg.code == "MSG" and Bot.proper_command(msg.json["message"], "!give_token")
