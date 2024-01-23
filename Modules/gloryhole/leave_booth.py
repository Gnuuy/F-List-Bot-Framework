from BotState import Bot
from BotSingleton import BotSingleton


HasHelpInfo = True
command_name = "!leave_booth"
command_description = "Leave the booth you're currently in."
bot_instance = BotSingleton()
room = bot_instance.room

def handler(msg_pipe):
    msg = msg_pipe.get()

    if msg.code == "PRI":
        character = msg.json["character"]

        # Find the booth that the character is in
        for booth in Bot.booths:
            if character in booth.occupants:
                # Remove the character from the booth
                booth.occupants.remove(character)
                booth.description = ""
                booth.participants = []
                booth.maxParticipants = 1
                Bot.send_out(Bot.Message(code="PRI", json={"message": "You have left the booth.\n If you have the spare time, we'd greatly appreciate your feedback. Use !feedback <message> if you wish to help improve this bot!", "recipient": character}))
                Bot.send_out(Bot.Message(code="MSG", json={"message": "Gloryhole #%d is once more vacant." % booth.id, "channel": room}))
                return

        # If the character is not in any booth
        Bot.send_out(Bot.Message(code="PRI", json={"message": "You are not in any booth.", "recipient": character}))

def predicate(msg):
    return msg.code == "PRI" and msg.json["message"] == command_name