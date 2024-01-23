from BotState import Bot
from BotSingleton import BotSingleton

# Configuration and setup
HasHelpInfo = True
command_name = "!kick"
command_description = "Remove a participant from a booth."
bot_instance = BotSingleton()
room = bot_instance.room
moderators = bot_instance.moderators

# Handler function for processing messages
def handler(msg_pipe):
    msg = msg_pipe.get()

    # Only respond to public messages
    if msg.code == "MSG":
        character = msg.json["character"]
        parts = msg.json["message"].split()

        # Check if the user is a moderator
        if character not in moderators:
            response = "You do not have the privilege to use this command."
            Bot.send_out(Bot.Message(code="MSG", json={"message": response, "channel": room}))
            return

        if len(parts) != 2:
            Bot.send_out(Bot.Message(code="MSG", json={"message": "Invalid command format. Use '!kick <participant name>'.", "channel": room}))
            return

        participant_to_kick = parts[1]

        # Iterate over all booths to find and remove the participant
        participant_found = False
        for booth in Bot.booths:
            if participant_to_kick in booth.participants:
                booth.participants.remove(participant_to_kick)
                participant_found = True

                # Notify the public channel
                response = f"Participant {participant_to_kick} removed from Gloryhole #{booth.id}."
                Bot.send_out(Bot.Message(code="MSG", json={"message": response, "channel": room}))

                # Notify the occupant
                occupant_message = f"A participant has been removed from your booth."
                if booth.occupants:
                    for occupant in booth.occupants:
                        Bot.send_out(Bot.Message(code="PRI", json={"message": occupant_message, "recipient": occupant}))

                break

        if not participant_found:
            response = f"No participant named '{participant_to_kick}' found at any Gloryhole."
            Bot.send_out(Bot.Message(code="MSG", json={"message": response, "channel": room}))


def predicate(msg):
    return msg.code == "MSG" and msg.json["message"].startswith(command_name)