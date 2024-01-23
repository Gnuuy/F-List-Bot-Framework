from BotState import Bot
from BotSingleton import BotSingleton

HasHelpInfo = True
command_name = "!scribble"
command_description = "Scribble a message on a gloryhole wall!"
bot_instance = BotSingleton()
room = bot_instance.room

def handler(msg_pipe):
    msg = msg_pipe.get()

    if msg.code == "MSG":
        # Split command into parts
        parts = msg.json["message"].split(maxsplit=2)

        if len(parts) < 3:
            # Either booth number or graffiti text or both not provided
            Bot.send_out(Bot.Message(code="MSG", json={"message": "Invalid command format. Use '!scribble <booth_number> <scribble text>'.", "channel": room}))
            return

        try:
            booth_number = int(parts[1]) - 1  # Convert to zero-based index
            graffiti_text = parts[2]

            if 0 <= booth_number < len(Bot.booths):
                # Add graffiti to the specified booth
                Bot.booths[booth_number].graffiti.append(graffiti_text)
                Bot.send_out(Bot.Message(code="MSG", json={"message": f"Graffiti added to Gloryhole #{booth_number + 1}.", "channel": room}))
            else:
                # Invalid booth number
                Bot.send_out(Bot.Message(code="MSG", json={"message": "Invalid booth number.", "channel": room}))

        except ValueError:
            # Handle non-integer booth numbers
            Bot.send_out(Bot.Message(code="MSG", json={"message": "Invalid booth number. Please enter a valid number.", "channel": room}))

def predicate(msg):
    return msg.code == "MSG" and msg.json["message"].startswith(command_name)