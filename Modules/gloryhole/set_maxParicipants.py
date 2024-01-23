from BotState import Bot

HasHelpInfo = True
command_name = "!set_customers"
command_description = "Set the maximum number of customers you can serivce at once booth you're currently in."

customer_limit = 5

def handler(msg_pipe):
    msg = msg_pipe.get()

    parts = msg.json["message"].split()

    # Check for correct command format
    if len(parts) != 2:
        Bot.send_out(Bot.Message(code="PRI", json={"message": "Invalid command format. Use '!set_customers <number>'.", "recipient": msg.json["character"]}))
        return

    try:
        new_max = int(parts[1])
    except ValueError:
        # Handle non-integer inputs
        Bot.send_out(Bot.Message(code="PRI", json={"message": "Invalid number format. Please enter a valid number.", "recipient": msg.json["character"]}))
        return

    # Validate the number range
    if new_max < 1 or new_max > customer_limit:
        Bot.send_out(Bot.Message(code="PRI", json={"message": "Invalid number. Please choose a value between 1 and 4.", "recipient": msg.json["character"]}))
        return

    character = msg.json["character"]
    booth_found = False

    for booth in Bot.booths:
        # Check if the user is an occupant of the booth
        if character in booth.occupants:
            booth.maxParticipants = new_max
            booth_found = True
            Bot.send_out(Bot.Message(code="PRI", json={"message": f"You slide open a few more sockets. You can now service up to {new_max} customers!", "recipient": character}))
            break

    if not booth_found:
        Bot.send_out(Bot.Message(code="PRI", json={"message": "You are not in a booth.", "recipient": character}))

def predicate(msg):
    return msg.code == "PRI" and msg.json["message"].startswith(command_name)