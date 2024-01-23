from BotState import Bot

HasHelpInfo = True
command_name = "!get_gloryholes"
command_description = "Get a list of all available gloryholes!"

def handler(msg_pipe):
    msg = msg_pipe.get()

    txt = "Available gloryholes:\n"

    first_unoccupied_booth = None

    for booth in Bot.booths:
        numParticipants = len(booth.participants)
        graffiti = ", ".join(booth.graffiti)
        description = f"\n--Description: \"{booth.description}\"" if booth.description else ""
        participants = ", ".join(booth.participants)

        if booth.occupants == [] and first_unoccupied_booth is None:
            first_unoccupied_booth = booth
        elif booth.occupants != []:
            status = "[b][color=yellow]WAITING[/color][/b]" if participants == "" else "[b][color=green]IN USE[/color][/b]"
            participants_info = f" [color=green][Participants: \"{participants}\"][/color]" if participants else ""
            txt += f"[{numParticipants}/{booth.maxParticipants}]Gloryhole #{booth.id} - {status}{participants_info} - Scribbles: \"{graffiti}\"{description}\n"

        #Formatting:
        #[0/3]Gloryhole #1 - WAITING - Scribble: "I was here"
        # Description "I am here"
        #[1/2]Gloryhole #2 - IN USE - Participants: "John, Jane" - Scribble: "I was here"

    if first_unoccupied_booth:
        graffiti = ", ".join(first_unoccupied_booth.graffiti)
        description = f"\n Description: \"{first_unoccupied_booth.description}\"" if first_unoccupied_booth.description else ""
        txt += f"[{numParticipants}/{booth.maxParticipants}]Gloryhole #{first_unoccupied_booth.id} - [b]EMPTY[/b] - Scribbles: \"{graffiti}\"{description}\n"
    txt = "[spoiler]" + txt + "[/spoiler]"
    Bot.send_out(Bot.Message(code="MSG", json={"message": txt, "channel": msg.json["channel"]}))

def predicate(msg):
    return msg.code == "MSG" and Bot.proper_command(msg.json["message"], command_name)
