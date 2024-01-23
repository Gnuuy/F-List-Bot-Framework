from BotState import Bot
from BotSingleton import BotSingleton
import random

HasHelpInfo = True
command_name = "!dare"
command_description = "Get a random starter for an oral-based scene."
bot_instance = BotSingleton()
room = bot_instance.room

# I totally stole this code from the gnuuy omigosh

messages = [
    "Blindfold yourself, then find someone make out with for at least 60 seconds!",
    "See how long you can hold your breath with someone's dick in your throat.",
    "Blindfold yourself, then find some dick to suck by any means necessary!",
    "Perform a striptease in front of someone to get them ready to treat them to some oral sex.",
    "Incorporate food (Chocolate, whipped cream, Honey...) into oral sex involving someone's %s as the focus!",
    "Bring a vibrator to tease someone's body while performing oral on them!",
    "Purposefully perform slow to tease your partner during oral, bringing them to climax in an intense fashion!",
    "Use as much dirty-talk as you can while suckin' some dick! Or eating a gal out, if that's your preference.",
    "Handcuff yourself, then perform oral on someone!",
    "Get into an a-typical position during oral! Try to 69 them, or put your head in their lap while they can finger you on the couch, or something else to that effect!",
    "Perform some act of oral while letting the person you perform on take a video! Smile for the camera!",
    "Use any kind of toy during oral sex!",
    "Give someone a handjob, and keep your mouth on the tip as long as you can!",
    "Have someone straddle your face to give you full access to their package for you to lick, suck, etc!",
    "Make it a threesome! Find someone else to get two mouths on one person!",
    "Hold someone else' head and help them suck some dick!",
    "Hold someone else' head and help them eat out a gal!",
    "Blindfold someone else, then use your mouth to please them!",
    "Blow someone with a mirror beside you to show a nice reflection! Grab a phone, and record it too!"
    ]

# Variable to track the last message sent
last_message = None

def handler(msg_pipe):
    global last_message

    msg = msg_pipe.get()

    # Select a random message different from the last one sent
    available_messages = [m for m in messages if m != last_message]
    selected_message = random.choice(available_messages)

    # Update the last message sent
    last_message = selected_message

    bodyparts = ["Mouth", "Dick", "Pussy", "Fingers", "Nipples", "Breasts", "Clitoris", "Abs"]
    if "%s" in selected_message:
        selected_message = selected_message % (random.choice(bodyparts))

    # Check if the message is private or public, and respond accordingly
    if msg.code == "PRI":
        # Respond to a private message
        Bot.send_out(Bot.Message(code="PRI", json={"message": selected_message, "recipient": msg.json["character"]}))
    elif msg.code == "MSG":
        # Respond to a public message
        Bot.send_out(Bot.Message(code="MSG", json={"message": selected_message, "channel": room}))


def predicate(msg):
    return (msg.code == "PRI" or msg.code == "MSG") and msg.json["message"].startswith(command_name)
