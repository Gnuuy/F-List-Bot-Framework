from BotState import Bot
from BotSingleton import BotSingleton

HasHelpInfo = True
command_name = "!kick"
command_description = "Remove the occupant from a booth."
bot_instance = BotSingleton()
room = bot_instance.room

# List of moderators
moderators = ["Moo", "Keyah","Kemonomimi GM", "Captain Eberswalde", "Mayhem Maid", "Fetch me their souls", "Cassandra Star", "Fellation", "Prolific", "Leuna Madra", "Clari", "Brenda", "Petulant", "Kemonomimi Hub", "Sarathiel", "Nine Lives", "Red Shadowscale", "Ellis Ailven", "Red Eyed Bunny", "ElpheIt Valentine"]

def handler(msg_pipe):
    msg = msg_pipe.get()

    character = msg.json["character"]
    parts = msg.json["message"].split()

    # Check if the user is a moderator
    if character not in moderators:
        response = "You do not have the privilege to use this command."
        Bot.send_out(Bot.Message(code="PRI", json={"message": response, "recipient": character}))
        return

    if len(parts) != 2:
        Bot.send_out(Bot.Message(code="PRI", json={"message": "Invalid command format. Use '!remove <booth_number>'.", "recipient": character}))
        return

    try:
        booth_number = int(parts[1]) - 1  # Convert to zero-based index

        if 0 <= booth_number < len(Bot.booths):
            # Remove the occupant from the booth
            if Bot.booths[booth_number].occupants:
                removed_occupant = Bot.booths[booth_number].occupants.pop(0)
                response = f"Occupant {removed_occupant} removed from Booth #{booth_number + 1}."
            else:
                response = f"Booth #{booth_number + 1} is already empty."
        else:
            response = "Invalid booth number."

        Bot.send_out(Bot.Message(code="PRI", json={"message": response, "recipient": character}))

    except ValueError:
        Bot.send_out(Bot.Message(code="PRI", json={"message": "Invalid booth number format. Please enter a valid number.", "recipient": character}))

def predicate(msg):
    return msg.code == "PRI" and msg.json["message"].startswith(command_name)