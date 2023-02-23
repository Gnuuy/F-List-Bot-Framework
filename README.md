# F-List-Bot-Framework
This repository contains a framework that is meant to be utilized for developments of new bots on F-list, making it easy for someone with python knowledge to create a bot within f-chat.

To get started, please read:
https://wiki.f-list.net/F-Chat_Protocol

And use this as reference as you wish for chat protocol and bot rules:

https://wiki.f-list.net/F-Chat_Protocol#Bots

https://wiki.f-list.net/F-Chat_Client_Commands

https://wiki.f-list.net/F-Chat_Server_Commands

https://toys.in.newtsin.space/api-docs/ These are some AWESOME docs on F-list API in general!

## Installation
* Download this repo.
* Ensure you have python 3+
* Run `pip install -r requirements.txt` within the base folder of the bot.
* Fill out your information within bot_credentials.txt (Do not share it with others!)
* * "username" should be your account username.
* * "password" should be your account password.
* * "bot_name" should be the character name of the bot.
* * "bot_user_agent_name" should be something friendly that allows F-list staff to distinguish your bot. This is not seen publicly by any chat users.
* * * It should be something like "[bot-name] For [bot-room]" or "[bot-name] Test bot for [Your character name]"
* * "bot_version" should be something like "0.0.1" or "1.0.0" or "23.44.55"
* Run `python bot.py` and watch it login! The bot will respond to !help in its PMs!

## Development, Adding new Modules to your new bot!

By default, it comes with the following modules:
* [chat_write_to_logfile.py](Modules/chat_write_to_logfile.py) (Logs all chat messages received within rooms to a folder in the base folder of the bot!)
* [help_command.py](Modules/help_command.py) (A !help command that will list all commands currently loaded into the bot's memory IF AND ONLY IF the command has been specified to have help info within its module.)
* [login_to_room.py](Modules/login_to_room.py) (A module that makes your bot login to your room upon login!)
* [pin_responder.py](Modules/pin_responder.py) (A module that handles responses to F-list's PIN protocol, a protocol that makes sure your bot client is still online. This is required for the bot to function.)
* [print_to_console.py](Modules/print_to_console.py) (A module that logs all chat commands to your console!)
* [simple_echo_command.py](Modules/simple_echo_command.py) (A simple echo command which you can use by typing !echo [bla bla bla...] to the bot!)

## The `Message` object...
This bot will pass objects that are used to parse F-list chat protocol and make them easy to handle. F-list chat protocol defines a server/client command as:

```
XXX {"property":"value","anotherproperty":"value"}
```

Where XXX is the code of the command, followed by the rest of the content, which is in JSON format.

Message objects passed to your module have two attributes of concern for you to easily access these elements:

```
msg.code [This is a string]
msg.json [This is a json dictionary]
```

Lets say that the user `Moo` sends the bot a PM. The bot will get the following protocol message sent to it:
```
PRI { "character": "Moo", "message": "Hiya, and thanks for using my framework! I hope it helps you!" }
```
Where "character" is the sender to your bot, and "message" is the message they sent.

Your message object's `code` will be equal to "PRI", and your json dictionary will be all of the json afterwards. If you want to grab the message from that private message you just received, just do:

```
message_text = msg.json["message"]
print(message_text)
```

The above snippet will print whatever private messages you're sent to console! It's a simple, easy logger implemented via the bot.

Lucky for you, you've already got yourself a console logger for MSG commands as-is, written in [print_to_console.py](Modules/print_to_console.py). It's a good example!
### Modules

Obviously, you want to extend further functionality to this bot so that you can make it your own!

Fear no more, for this is exactly why I wrote this project the way I have. You may already see that this bot contains a folder named `Modules`, in which you will find several python files that contain code modules for the bot to run. You may also see that they have a very specific structure, which will be explained below.

Adding a new module is relatively simple.

First, enter [/Modules](/Modules)

Create a new file, of which you may name it anything you'd like. Say, `my_new_module.py` (Something descriptive of what it does helps, as it's what is logged to your console occasionally for debugging purposes!)

A module requires the following items to be considered valid by the bot:

* A global boolean variable defined, named `HasHelpInfo`
* * If this is set to `True`, you must also include two other global variables: `command_name`(a string) and `command_description`(a string), as the bot uses this to fill out help information for the !help command!
* A python function defined in the global scope, with a signature of `handler(msg_queue)`
* A python function defined in the global scope, with a signature of `predicate(msg)`

And that's it! Doing so allows the bot to **automatically** load your module from now on into memory each time it starts up!

Now, let's talk about what the above things are for, particularly the two functions up above.

## `predicate(msg)`

This function is important. A predicate function is something that the module dispatcher within the bot calls each time it has a new message within it's input queue. Particularly, your predicate function tells the bot "I am interested in messages and want them to be sent to me if they reach X criteria!"

So, what does this look like?

As per F-list Chat protocol, `MSG` codes are sent only for messages send within chat channels, either public or private. If you want to make a module, and tell the bot to send it anything from F-list that is a chat-room message, you would put this in your predicate function:

```
def predicate(msg):
  return msg.code == "MSG"
```

The above predicate function returns `True` if the message in question has a code that is equal to "MSG", which is a message within a chat room! Now the bot will send any F-list protocol "MSG" messages that you can then parse and make the bot respond to appropriately within your `handler` function!

You can get as complex as you'd like with this, of course. Make your predicate functions complex, if you want to have some complex logic behind when a particular F-list protocol message should be sent to your module's `handler` function! 

## `handler(msg_queue)`

This is your primary logic that you'll be keeping within your function. The message queue parameter here is literally a python queue object - of which you must call the `get()` method to retrieve messages passed to your module. Generally, this'll look like putting the line `msg = msg_queue.get()` at the beginning of your handler() function, so that your handler function ALWAYS waits for the messages it is interested in. (But don't worry, this will only pause the thread for your module alone - it's efficient!

This function can make the bot do **anything.** You can tell it to write files to disk. You can have it print messages. You can have it respond by sending F-list protocol messages of your own -- the possibilities are endless! 

For now, though, lets focus on something simple - lets look at writing a handler function that logs all messages received to disk, in a file.

```
import datetime

def handler(msg_pipe):
    msg = msg_pipe.get() # Takes the message passed to your handler out of the queue.
           
    logfile = open("log.txt" % msg.json["channel"], "a", encoding="utf-8") # Open a file with utf-8 encoding for appending.
    logfile.write("[%s] %s: %s\n" % (str(datetime.datetime.now()), msg.json["character"], msg.json["message"])) # Write a timestamped version of what was sent to that file!
```

**It's just that simple!**

This bot's basically gone and abstracted all the messiness of handling with protocol away from you - so that you can just focus on writing logic for your bot that responds to messages sent to your modules, as you define them. Take a look at some other examples - make some complex modules! The world is your apple!

## What's this wacky `from BotState import Bot` import I see at the top of some modules?!

Doing this within a module imports a global variable named `Bot`... what's stored in that? It's a reference (pointer) to the main, running bot module's global scope! This allows you to access functions, global variables, and other things located within the running state of [bot.py](bot.py)! 

Within [bot.py](bot.py) there a few helpful global variables, and functions you may want to keep track of which may prove useful to you over time.

### [Bot.Message](bot.py#L121-L152)
There is a `Message` class defined within bot.py, which is something you can call to instantiate your own Message objects as stated in the spec above! An example of doing so will be as such:

```
my_created_message = Bot.Message(code="MSG", json={"channel": "development", "message": "Hi there, I'm developing a bot!"})
```

You've now created your own `Message` object. What can you do with this? You can convert it to a string, of course! Doing so via:

```
msg_string = str(my_created_message)
```

Will convert the above message you just created into a message compatible with F-list's API protocol to be sent back to F-chat's server! It'll convert the above thing into:
`MSG {"channel": "development", "message": "Hi there, I'm developing a bot!"}` -- This is a valid F-list chat command that can be sent back to F-list's servers.

### [Bot.send_out(message_object)](bot.py#L154-L156)

You may call this method to send a message object constructed via the [Bot.Message](bot.py#L121-L152) class out of the bot back to F-chat's servers. It's just that easy!

### [Bot.get_ticket()](bot.py#L79-L101)

Call this method if you'd like to fetch a chat ticket for your current session to hit JSON API endpoints from F-list yourself with the requests library, as per https://wiki.f-list.net/Json_endpoints#Acquiring_a_ticket.

# FAQ

### What if I write bad code in one of my modules? What if my module crashes the bot?!

Your bot will not shut off. Instead, the bot will shut down your module, write to an error log in the base directory to tell you about it, and not boot up your module again until you restart the bot.

### What if I want to tell the bot to kill my module and drop it out of memory?

Write `exit()` in your module somewhere within your handler() function. This will cause the thread for your module to die, and the dispatcher for the bot will handle it appropriately.
