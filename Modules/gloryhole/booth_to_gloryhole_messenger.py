from BotState import Bot
from BotSingleton import BotSingleton

HasHelpInfo = False
bot_instance = BotSingleton()
room = bot_instance.room

def handler(msg_pipe):
    msg = msg_pipe.get()

    if msg.code == "PRI" and msg.json["message"].startswith("/me"):
        character = msg.json["character"]
        forwarded_message = msg.json["message"]

        # Find the booth the character is an occupant of
        for booth in Bot.booths:
            if character in booth.occupants:
                # Check if there are participants in the booth
                if booth.participants:
                    # List both occupants and participants
                    occupants_list = ", ".join(booth.occupants)
                    participants_list = ", ".join(booth.participants)
                    public_message = f"/me [color=green][Participants: {participants_list}][/color] Gloryhole #{booth.id} {forwarded_message[4:]}" 

                    # Forward the message to the public channel
                    Bot.send_out(Bot.Message(code="MSG", json={"message": public_message, "channel": room}))
                else:
                    # Send a private message back if there are no participants
                    wait_message = "Please wait for a participant to join the booth before sending public messages."
                    Bot.send_out(Bot.Message(code="PRI", json={"message": wait_message, "recipient": character}))
                break

                
def predicate(msg):
    return msg.code == "PRI" and msg.json["message"].startswith("/me")
