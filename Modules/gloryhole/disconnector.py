from BotState import Bot
from BotSingleton import BotSingleton
import threading

HasHelpInfo = False
bot_instance = BotSingleton()
room = bot_instance.room

# Time limit for disconnection (in seconds)
DISCONNECT_TIME_LIMIT = 600  # 10 minutes

# Structure to keep track of disconnected users and their timers
disconnected_users = {}

def handle_disconnection(character):
    # Handles the disconnection logic for a character.
    if character in disconnected_users:
        booth_id, _ = disconnected_users[character]
        booth = next((b for b in Bot.booths if b.id == booth_id), None)

        if booth:
            message_for_channel = ""
            message_for_occupants = ""
            if character in booth.occupants:
                booth.occupants.remove(character)
                booth.description = ""
                booth.maxParticipants = 1
                message_for_channel = f"Gloryhole #{booth.id} is now vacant due to disconnection."
            elif character in booth.participants:
                booth.participants.remove(character)
                message_for_channel = f"Gloryhole #{booth.id} has one less participant due to disconnection."
                message_for_occupants = f"A participant has been removed due to disconnection."

            if message_for_channel:
                # Notify the channel about the removal
                Bot.send_out(Bot.Message(code="MSG", json={"message": message_for_channel, "channel": room}))

            if message_for_occupants:
                # Notify all occupants about the participant disconnection
                for occupant in booth.occupants:
                    Bot.send_out(Bot.Message(code="PRI", json={"message": message_for_occupants, "recipient": occupant}))

        del disconnected_users[character]

def on_disconnect(character):
    # Starts a timer when a character disconnects.
    booth = next((b for b in Bot.booths if character in b.occupants or character in b.participants), None)
    if booth:
        timer = threading.Timer(DISCONNECT_TIME_LIMIT, handle_disconnection, args=[character])
        timer.start()
        disconnected_users[character] = (booth.id, timer)

        message_for_channel = ""
        message_for_occupants = ""
        if character in booth.occupants:
            message_for_channel = f"Gloryhole #{booth.id} occupant has disconnected. Awaiting reconnection..."
        elif character in booth.participants:
            message_for_channel = f"Gloryhole #{booth.id} participant has disconnected. Awaiting reconnection..."
            message_for_occupants = f"A participant has disconnected."

        if message_for_channel:
            # Notify the channel about the disconnection
            Bot.send_out(Bot.Message(code="MSG", json={"message": message_for_channel, "channel": room}))

        if message_for_occupants:
            # Notify all occupants about the participant disconnection
            for occupant in booth.occupants:
                Bot.send_out(Bot.Message(code="PRI", json={"message": message_for_occupants, "recipient": occupant}))

        print(f"[SYSTEM]: {character} has disconnected.")

def on_reconnect(character):
    # Cancels the disconnection timer if the character reconnects.
    if character in disconnected_users:
        booth_id, timer = disconnected_users[character]
        timer.cancel()
        del disconnected_users[character]

        booth = next((b for b in Bot.booths if b.id == booth_id), None)
        if booth:
            message_for_channel = ""
            message_for_occupants = ""
            is_occupant = character in booth.occupants
            is_participant = character in booth.participants

            if is_occupant or is_participant:
                if is_occupant:
                    message_for_channel = f"Gloryhole #{booth_id} occupant has reconnected."
                if is_participant:
                    message_for_channel = f"Gloryhole #{booth_id} participant has reconnected."
                    message_for_occupants = f"A participant has reconnected."

                if message_for_channel:
                    # Send a message indicating the user has reconnected
                    Bot.send_out(Bot.Message(code="MSG", json={"message": message_for_channel, "channel": room}))

                if message_for_occupants:
                    # Notify all occupants about the participant reconnection
                    for occupant in booth.occupants:
                        Bot.send_out(Bot.Message(code="PRI", json={"message": message_for_occupants, "recipient": occupant}))

        print(f"[SYSTEM]: {character} has reconnected.")

def handler(msg_pipe):
    msg = msg_pipe.get()

    # Check for disconnection
    if msg.code == "FLN" and 'character' in msg.json:
        character = msg.json["character"]
        on_disconnect(character)

    # Check for reconnection
    elif msg.code == "NLN" and 'identity' in msg.json:
        character = msg.json["identity"]
        on_reconnect(character)

def predicate(msg):
    return msg.code == "FLN" or (msg.code == "NLN" and msg.json.get("identity") in disconnected_users)