from BotState import Bot
from BotSingleton import BotSingleton

HasHelpInfo = True
command_name = "!enter_booth"
command_description = "Enter a booth."
bot_instance = BotSingleton()
room = bot_instance.room

def bookmark_user(character):
    # Implementation to bookmark the user using F-list's API
    # Placeholder function - Replace with actual API call as per F-list's documentation
    pass

def handler(msg_pipe):
    msg = msg_pipe.get()

    if msg.code == "PRI":
        parts = msg.json["message"].split()
        if len(parts) == 2 and parts[0] == command_name.split()[0]:
            try:
                booth_number = int(parts[1]) - 1  # Convert to zero-based index

                if 0 <= booth_number < len(Bot.booths):
                    character = msg.json["character"]

                    if any(character in booth.occupants for booth in Bot.booths):
                        Bot.send_out(Bot.Message(code="PRI", json={"message": "You are already in a booth.", "recipient": character}))
                    elif Bot.booths[booth_number].occupants == []:
                        Bot.booths[booth_number].occupants.append(character),

                        # Respond to the character
                        enter_message = f"""
[color=pink]You enter the booth labelled {booth_number + 1}, slide the door shut behind you and, with an audible click, turn the lock to[/color] [color=red]OCCUPIED[/color][color=pink]! Now you just have to wait for your first customer[/color].

By default, your booth's description is blank. To set a description for your booth to entice potential customers, type !set_description <message>.

By default, you can service one customer at a time. To increase the amount of customers you can service at once, type !set_customers <number>. Limit is 4 at once.

To leave the booth, type !leave_booth.
                        """
                        Bot.send_out(Bot.Message(code="PRI", json={"message": enter_message, "recipient": character}))

                        # Notify the channel
                        Bot.send_out(Bot.Message(code="MSG", json={"message": f"A soft metallic click emits from Gloryhole #{booth_number + 1}; service is waiting..", "channel": room}))
                    else:
                        Bot.send_out(Bot.Message(code="PRI", json={"message": "You cannot enter a booth that is occupied.", "recipient": character}))
                else:
                    Bot.send_out(Bot.Message(code="PRI", json={"message": "Invalid booth number.", "recipient": character}))
            except ValueError:
                Bot.send_out(Bot.Message(code="PRI", json={"message": "Invalid command format.", "recipient": character}))
                
def predicate(msg):
    return msg.code == "PRI" and Bot.proper_command(msg.json["message"], command_name)