from BotState import Bot

HasHelpInfo = True
command_name = "!remove_scribble"
command_description = "Removes a Scribble from a Gloryhole."

def send_response(msg, response):
    # Function to send response based on message type
    if msg.code == "PRI":
        # Send private response
        Bot.send_out(Bot.Message(code="PRI", json={"message": response, "recipient": msg.json["character"]}))
    else:
        # Send public response
        Bot.send_out(Bot.Message(code="MSG", json={"message": response, "channel": msg.json["channel"]}))

def handler(msg_pipe):
    msg = msg_pipe.get()

    parts = msg.json["message"].split()

    if len(parts) != 3:
        # Invalid command format
        response = "Invalid command format. Use '!remove_scribble <number> <scribble index>'."
        send_response(msg, response)
        return

    try:
        booth_number = int(parts[1]) - 1  # Convert to zero-based index
        graffiti_index = int(parts[2]) - 1 # Convert to zero-based index

        if 0 <= booth_number < len(Bot.booths):
            if 0 <= graffiti_index < len(Bot.booths[booth_number].graffiti):
                # Remove graffiti from the specified booth
                del Bot.booths[booth_number].graffiti[graffiti_index]
                response = f"Scribble removed from Gloryhole #{booth_number + 1}."
            else:
                # Invalid graffiti index
                response = "Invalid Scribble index."
        else:
            # Invalid booth number
            response = "Invalid booth number."

        send_response(msg, response)

    except ValueError:
        # Handle non-integer values
        response = "Invalid booth number or scribble index. Please enter valid numbers."
        send_response(msg, response)

def predicate(msg):
    return (msg.code == "MSG" or msg.code == "PRI") and msg.json["message"].startswith(command_name)