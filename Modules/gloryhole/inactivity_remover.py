from BotState import Bot
from BotSingleton import BotSingleton
import threading

HasHelpInfo = False
bot_instance = BotSingleton()
room = bot_instance.room

# Time limits for warning and removal due to inactivity (in seconds)
INACTIVITY_WARNING_TIME = 60 * 50  # 50 minutes for warning
INACTIVITY_REMOVAL_TIME = 60 * 60  # 60 minutes for removal

# Structure to keep track of inactive users and their timers
inactive_users = {}

def handle_inactivity_warning(character):
    # Handles warning a character about impending removal due to inactivity.
    if character in inactive_users:
        booth_id, _, _ = inactive_users[character]
        # Send a warning message
        Bot.send_out(Bot.Message(code="PRI", json={"message": "You have been inactive for 50 minutes. You will be removed from the booth in 10 minutes if there is no activity. Just write to me!", "recipient": character}))
        # Reset the timer for final removal
        final_timer = threading.Timer(INACTIVITY_REMOVAL_TIME - INACTIVITY_WARNING_TIME, handle_inactivity_removal, args=[character])
        final_timer.start()
        # True indicates warned
        inactive_users[character] = (booth_id, final_timer, True)

def handle_inactivity_removal(character):
    # Handles the removal of a character due to inactivity.
    if character in inactive_users:
        booth_id, _, _ = inactive_users[character]
        booth = next((b for b in Bot.booths if b.id == booth_id), None)

        if booth and character in booth.occupants:
            booth.occupants.remove(character)
            booth.description = ""
            booth.participants = []
            booth.maxParticipants = 1
            # Notify the user about the removal
            Bot.send_out(Bot.Message(code="PRI", json={"message": "You have been removed from the booth due to inactivity.", "recipient": character}))
            # Notify the channel about the vacancy
            Bot.send_out(Bot.Message(code="MSG", json={"message": f"Gloryhole #{booth_id} is now vacant due to inactivity.", "channel": room}))

        del inactive_users[character]

def on_inactivity_detected(character):
    # Starts a timer when a character is marked as inactive.
    booth = next((b for b in Bot.booths if character in b.occupants), None)
    if booth:
        timer = threading.Timer(INACTIVITY_WARNING_TIME, handle_inactivity_warning, args=[character])
        timer.start()
        inactive_users[character] = (booth.id, timer, False)  # False indicates no warning yet

def on_activity_resumed(character):
    # Resets the inactivity timer if the character becomes active again.
    if character in inactive_users:
        booth_id, timer, warned_status = inactive_users[character]
        timer.cancel()
        del inactive_users[character]
        # Send activity detected message only if they were warned
        if warned_status:
            Bot.send_out(Bot.Message(code="PRI", json={"message": "I can see that you're typing. [eicon]ellurk[/eicon] I have reset your inactivity timer!", "recipient": character}))

def handler(msg_pipe):
    msg = msg_pipe.get()

    # Check for inactivity status
    if msg.code == "TPN" and 'character' in msg.json:
        character = msg.json["character"]
        if msg.json["status"] == "clear":
            on_inactivity_detected(character)
        elif msg.json["status"] == "typing":
            on_activity_resumed(character)

def predicate(msg):
    return msg.code == "TPN" and ('character' in msg.json) and (msg.json["status"] in ["clear", "typing"])