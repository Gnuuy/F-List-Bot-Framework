from BotState import Bot

HasHelpInfo = True
command_name = "!set_description"
command_description = "Change the description of the booth you're currently in."

def handler(msg_pipe):
    msg = msg_pipe.get()

    if msg.code == "PRI":
        character = msg.json["character"]

        # Splitting the message to extract the command and new description
        parts = msg.json["message"].split(maxsplit=1) 

        if len(parts) < 2:
            # If the new description is not provided
            Bot.send_out(Bot.Message(code="PRI", json={"message": "No description provided.", "recipient": character}))
            return

        new_description = parts[1]

        # Find the booth that the character is in
        for booth in Bot.booths:
            if character in booth.occupants:
                # Update the booth description
                booth.description = new_description
                Bot.send_out(Bot.Message(code="PRI", json={"message": "Booth description updated.", "recipient": character}))
                return

        # If the character is not in any booth
        Bot.send_out(Bot.Message(code="PRI", json={"message": "You are not in any booth.", "recipient": character}))

def predicate(msg):
    return msg.code == "PRI" and msg.json["message"].startswith(command_name)