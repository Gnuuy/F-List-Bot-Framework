from BotState import Bot
from BotSingleton import BotSingleton
import random

HasHelpInfo = True
command_name = "!gnuuy"
command_description = "Get a random message from the gnuuy!"
bot_instance = BotSingleton()
room = bot_instance.room

messages = [
    "Rock out with your gnuuy out! [eicon]elrock[/eicon]",
    "Remember to pet your local gnuuy! [eicon]ellurk[/eicon]",
    "Stay sweet, stay strong, stay hydrated. [i][b]Or else![/b][/i] [eicon]elgun[/eicon]",
    "Marry! [eicon]elsgun[/eicon]",
    "Divorce! [eicon]elsgun[/eicon]",
    "Marry again! [eicon]elsgun[/eicon]",
    "Divorce again! [eicon]elsgun[/eicon]",
    "Be wifeable, but be [b][i]ready[/i][/b]! [eicon]elsgun[/eicon]",
    "Be husbandable, but be [b][i]ready[/i][/b]! [eicon]elsgun[/eicon]",
    "Just a gnuuy trying to make it in a bnuuy world. [eicon]elcry[/eicon]",
    "Drink water. Stay hydrated. [eicon]elsip[/eicon]",
    "Be kind to yourself. Or I will do it for you! [eicon]elwinks[/eicon]",
    "Noes! [eicon]elnoes[/eicon]",
    "[eicon]eleep[/eicon]",
    "I am going to smooch you. [eicon]ellurk[/eicon]",
    "I found a cute. It's you! [eicon]elzoom[/eicon]",
    "It's an all-out gnuuy-out! [eicon]elrout[/eicon]",
    "Block this, you filthy casual! [eicon]elshoot[/eicon]",
    "Remember to [eicon]elpet[/eicon]! [sub]Just a sneaky message snuck in by Moo.[/sub]",
    "Sometimes I just like to watch. [eicon]elpopcorn[/eicon]",
    "[i]GoshIwantyoutokissme![/i] [eicon]elblush[/eicon]",
    "I don't know what a gnussy is, but it sounds delicious! [eicon]elpensive[/eicon]",
    "Only thing I smash is the controller [eicon]elmash[/eicon]",
    "[eicon]elreally[/eicon]",
    "You're a reason to get up in the morning! [eicon]elwow[/eicon]"
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

    # Check if the message is private or public, and respond accordingly
    if msg.code == "PRI":
        # Respond to a private message
        Bot.send_out(Bot.Message(code="PRI", json={"message": selected_message, "recipient": msg.json["character"]}))
    elif msg.code == "MSG":
        # Respond to a public message
        Bot.send_out(Bot.Message(code="MSG", json={"message": selected_message, "channel": room}))


def predicate(msg):
    return (msg.code == "PRI" or msg.code == "MSG") and msg.json["message"].startswith(command_name)
