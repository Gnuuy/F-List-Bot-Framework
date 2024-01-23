from BotState import Bot
from BotSingleton import BotSingleton

HasHelpInfo = True
command_name = "!leave_gloryhole"
command_description = "Leave the gloryhole you're currently in."
bot_instance = BotSingleton()
room = bot_instance.room

def handler(msg_pipe):
    msg = msg_pipe.get()

    character = msg.json["character"]
    booth_found = False

    for booth in Bot.booths:
        if character in booth.participants:
            # Notify all occupants that a participant has left
            departure_message = f"Shadows disperse and light one more shine through the empty socket. Your customer has left!"
            for occupant in booth.occupants:
                if occupant != character:  # Optionally, don't send the message to the participant who is leaving
                    Bot.send_out(Bot.Message(code="PRI", json={"message": departure_message, "recipient": occupant}))

            booth.participants.remove(character)
            booth_found = True

            # Send a confirmation message to the participant who left
            Bot.send_out(Bot.Message(code="MSG", json={"message": "You have left the gloryhole.", "channel": room}))
            break


def predicate(msg):
    return msg.code == "MSG" and msg.json["message"] == command_name