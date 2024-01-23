from BotState import Bot
from BotSingleton import BotSingleton

HasHelpInfo = True
command_name = "!help"
command_description = ""
bot_instance = BotSingleton()
room = bot_instance.room

def handler(msg_pipe):
    msg = msg_pipe.get()

    # Lists to hold different types of commands
    private_cmds = []
    public_cmds = []
    dead_cmds = []

    # Categorize the commands based on keywords for exclusion
    for item in Bot.dispatcher.threadpool:
        if item.isPublicFacingCommand:
            if any(keyword in item.cmdname for keyword in ["description", "booth", "customer"]):
                private_cmds.append(item.cmdname)
            else:
                public_cmds.append(item.cmdname)

    # Categorize malfunctioning commands
    for item in Bot.dispatcher.deadmodules:
        if item.isPublicFacingCommand:
            dead_cmds.append(item.cmdname)

    # Constructing the message
    cmd_message = "Currently functioning commands:\n"
    if msg.code == "PRI":
        cmd_message += "[Private Commands: " + ", ".join(private_cmds) + "]\n"
    else:
        cmd_message += "[Public Commands: " + ", ".join(public_cmds) + "]\n"

    dead_cmd_message = "[Malfunctioning Commands: " + ", ".join(dead_cmds) + "]\n" if dead_cmds else "All good! No problems here :D"

    # Append contact information if there are dead commands
    if dead_cmds:
        dead_cmd_message += "[b]Please contact[/b] [user]Moo[/user] for assistance."

    # Prepare JSON payload
    json_payload = {"message": cmd_message + "\n\n" + dead_cmd_message}

    if msg.code == "PRI":
        json_payload["recipient"] = msg.json["character"]
    else:
        json_payload["channel"] = msg.json["channel"]

    # Send out the message
    Bot.send_out(Bot.Message(code=msg.code, json=json_payload))

def predicate(msg):
    return (msg.code == "MSG" or msg.code == "PRI") and Bot.proper_command(msg.json["message"], "!help")
