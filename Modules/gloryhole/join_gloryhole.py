from BotState import Bot
from BotSingleton import BotSingleton

HasHelpInfo = True
command_name = "!join_gloryhole"
command_description = "Join a gloryhole!"
bot_instance = BotSingleton()
room = bot_instance.room


def handler(msg_pipe):
    msg = msg_pipe.get()

    parts = msg.json["message"].split()

    if len(parts) != 2:
        Bot.send_out(Bot.Message(code="MSG", json={"message": "Invalid command format. Use '!join_booth <booth_number>'.", "channel": room}))
        return

    try:
        booth_number = int(parts[1]) - 1

        if 0 <= booth_number < len(Bot.booths):
            character = msg.json["character"]
            booth = Bot.booths[booth_number]

            # Check if the character is already participating in any booth
            for b in Bot.booths:
                if character in b.participants:
                    Bot.send_out(Bot.Message(code="MSG", json={"message": "You are already participating in a gloryhole. Please leave your current booth before joining another.", "channel": room}))
                    return

            # Check if the booth is at capacity
            if len(booth.participants) >= booth.maxParticipants:
                Bot.send_out(Bot.Message(code="MSG", json={"message": f"Gloryhole #{booth_number + 1} is at capacity.", "channel": room}))
                
                # Notify occupants that someone tried to join but was denied
                denial_message = f"A participant tried to join but your booth is at capacity. To change this, use the !set_maxparticipants <number> command."
                for occupant in booth.occupants:
                    Bot.send_out(Bot.Message(code="PRI", json={"message": denial_message, "recipient": occupant}))
                return

            # Check if the booth is unoccupied
            if not booth.occupants:
                Bot.send_out(Bot.Message(code="MSG", json={"message": "This gloryhole is currently closed as there are no occupants.", "channel": room}))
                return

            if character not in booth.participants:
                booth.participants.append(character)
                join_message = "A shadow flickers on the other side. Seems you have another customer!"

                # Notify all occupants in the booth
                for occupant in booth.occupants:
                    Bot.send_out(Bot.Message(code="PRI", json={"message": join_message, "recipient": occupant}))

                Bot.send_out(Bot.Message(code="MSG", json={"message": f"{character} joined Gloryhole #{booth_number + 1} as a participant.", "channel": room}))
            else:
                Bot.send_out(Bot.Message(code="MSG", json={"message": "You are already a participant.", "channel": room}))
        else:
            Bot.send_out(Bot.Message(code="MSG", json={"message": "Invalid gloryhole number.", "channel": room}))

    except ValueError:
        Bot.send_out(Bot.Message(code="MSG", json={"message": "Invalid gloryhole number. Please enter a valid number.", "channel": room}))


def predicate(msg):
    return msg.code == "MSG" and msg.json["message"].startswith(command_name)