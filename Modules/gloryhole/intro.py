from BotState import Bot

HasHelpInfo = True
command_name = "!intro"
command_description = "Provides an introduction to the Booth system"

def handler(msg_pipe):
    msg = msg_pipe.get()

    if (msg.code == "PRI" or msg.code == "MSG") and msg.json["message"].startswith("!intro"):
        # The user who sent the message
        character = msg.json["character"]
        intro_message = f"""
Hello {character}, your local gnuuy here to help you get started! [eicon]elwinks[/eicon]
            
The gloryhole is a place where you can anonymously have fun!

If you're like me and you enjoy the thrill of public play, but you're too shy to do it in front of 
people with your name on display--or simply enjoy the thrill of gloryholes--then this is the place for you!
[color=pink]
╔═════════════════════════════════════════╣ [b]BOOTHS[/b] ╠══════════════════════════════════════
║ Booths are private and is where you can service customers anonymously.
║
║ Your name will be displayed as Gloryhole #<Number> to others in the channel.
║ As an occupant you'll be interacting with booths to service customers! You can only occupy one booth at a time.
║
║[/color] [color=yellow]All interaction is done through me, the bot! Don't worry, it's all between you and me.[/color][color=pink]
║ Just send your commands to me, and I'll take care of the rest! Nobody but I will know who you are.
║
║[/color] [color=yellow]Messages starting with /me that you PM to me will be forwarded to the channel under the guise of your chosen booth's number.[/color][color=pink]
║
║ Example:
║ PM to me: /me makes a whole series of lewd noises.
║ In channel: Gloryhole #5 makes a whole series of lewd noises.
║
║ In order to send messages, you must have a customer. If you don't have one for your booth, just wait! They'll come soon enough.
║
║ [/color] [color=yellow]All commands containing the word 'booth' work in PMs with me. Not in the public channel.[/color][color=pink]
║ To get started type [/color][color=green]!get_booths[/color][color=pink] to get a list of available booths.
║            
║ To enter a booth, type [/color][color=green]!enter_booth[/color][color=pink] followed by the number of the booth you would like to occupy.
║ Example: !enter_booth 5
╚══════════════════════════════════════════════════════════════════════════════════════════
[/color]
[color=blue]
╔══════════════════════════════════════════╣ [b]GLORYHOLES[/b] ╠════════════════════════════════════
║ Gloryholes are public and is where you can receive service from a booth.
║
║ If you want to publically use a gloryhole, you can head on over to [session=Oral Addicts Anonymous]Oral Addicts Anonymous[/session] and 
║ type [/color][color=green]!get_gloryholes[/color][color=blue] to get a list of available gloryholes.
║
║ [/color] [color=yellow]All commands containing the word 'gloryhole' only works in the public channel.[/color][color=blue]
║ Once you find one that you like, type [/color][color=green]!join_gloryhole[/color][color=blue] followed by its number to start using it.
║ Example: !join_gloryhole 5
║
║[/color] [color=yellow]All messages you send in the channel that starts with /me will be forwarded to the occupant in the booth.[/color][color=blue]
║ Example: /me enjoys this.
║
║ To leave a gloryhole that you have joined, type [/color][color=green]!leave_gloryhole[/color][color=blue]
╚══════════════════════════════════════════════════════════════════════════════════════════
[/color]
If you wish to help improve this bot, you can use !feedback <message> to send in your experiences, bug reports, suggestions, ideas, etc!
Example: !feedback I want to help improve this bot!

Feel free to send a direct message to [user]ElpheIt Valentine[/user] if you have feedback, ideas or encounter critical issues.

But most of all -- have fun! [eicon]elheart[/eicon]"""

        # Send the intro message back to the user as a private message
        Bot.send_out(Bot.Message(code="PRI", json={"message": intro_message, "recipient": character}))



    
    
def predicate(msg):
    return (msg.code == "PRI" or msg.code == "MSG") and msg.json["message"].startswith(command_name)