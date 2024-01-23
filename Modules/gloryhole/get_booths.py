from BotState import Bot

HasHelpInfo = True
command_name = "!get_booths"
command_description = "Get a list of all available booths!"

def handler(msg_pipe):
    msg = msg_pipe.get()

    txt = "Here are the booths:\n" 

    # List all booths
    for booth in Bot.booths:
        status = "[b][color=green]AVAILABLE[/color][/b]" if booth.occupants == [] else "[b][color=red]OCCUPIED[/color][/b]"
        graffiti = ", ".join(booth.graffiti)
        description = f"\n Description: \"{booth.description}\"" if booth.description else ""
        txt += f"Booth #{booth.id} - {status} - Graffiti: \"{graffiti}\"{description}\n"

    # Send out the message as a private message
    Bot.send_out(Bot.Message(code="PRI", json={"message": txt, "recipient": msg.json["character"]}))

def predicate(msg):
    # Returns true if the message is private and contains the correct command
    return msg.code == "PRI" and Bot.proper_command(msg.json["message"], command_name)