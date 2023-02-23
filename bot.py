from time import sleep
from random import random
import requests
from lomond import WebSocket
from lomond.persist import persist
from multiprocessing import Lock
import json as jsonlib
import time
import multiprocessing as mp
import threading
import traceback
import socket
import os
import signal
import queue
import datetime
import pathlib
import sys
sys.path.insert(0, str(pathlib.Path("./Modules").resolve()))

bot_creds = open("bot_credentials.txt", "r").read()
creds = jsonlib.loads(bot_creds)

username = creds['username']
password = creds['password']
chat_url = 'wss://chat.f-list.net/chat2'
botname = creds['bot_name']
cname = creds["bot_user_agent_name"]
cversion = creds["bot_version"]



if creds['username'] == "" or creds['password'] == "" or creds['bot_name'] == "" or creds['bot_user_agent_name'] == "" or creds['bot_version'] == "" :
    print("You have not specified all the required info in bot_credentials.txt")
    exit()

# Set working dir to script dir
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

# You must press enter occasionally or the script will never unpause. 
# It will process things in-order from the time of when it paused though.
# This chunk of code under this if block disables that.
# https://stackoverflow.com/questions/73486528/python-script-pausing-in-cmd

if os.name != 'posix':
    

    import win32console as con

    # Set working dir to script dir
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)

    ENABLE_EXTENDED_FLAGS = 0x0080
    ENABLE_QUICK_EDIT_MODE = 0x0040 

    h = con.GetStdHandle(con.STD_INPUT_HANDLE)
    oldMode = h.GetConsoleMode()
    
    # Restore old console mode on CTRL-C 
    def handler(signum, frame):
        h.SetConsoleMode(oldMode)
        exit()

    signal.signal(signal.SIGINT, handler)

    # Modify console mode to disable quick edit mode
    h.SetConsoleMode((oldMode | ENABLE_EXTENDED_FLAGS) & ~ENABLE_QUICK_EDIT_MODE)
    
########################################################################################



######################################################################################### UTILITIES #########################################################################################

def getTicket():
    global ticketlock
    global ticket
    
    ticketlock.acquire()
    # 25 mins in seconds
    if time.time() - tickettime < 1500 and ticket != "":
        ticketlock.release()
        return ticket
    ticketlock.release()
        
    request_body = {'account': username, 'password': password, 'no_characters': 'true', 'no_bookmarks': 'true', 'no_friends': 'true'}
    response = requests.post('https://www.f-list.net/json/getApiTicket.php', data=request_body)
    
    ticketlock.acquire()
    try:
        ticket = response.json()['ticket']
    except:
        print(response.json())
        exit()
    ticketlock.release()
    
    return ticket
    
def handleFatalErrMessage(message):
    if message.code == "ERR":
        print("FATAL, F-LIST SERVERS ARE KICKING US FOR SOME REASON")
        print("EVENT TEXT BELOW")
        print(message.raw)
        
        print("COMMON ERRORS ARE:")
        print("""
                2: The server is full and not able to accept additional connections at this time.
                9: The user is banned.
                30: The user is already connecting from too many clients at this time.
                31: The character is logging in from another location and this connection is being terminated.
                33: Invalid authentication method used.
                39: The user is being timed out from the server.
                40: The user is being kicked from the server.
                """)
        exit()
        
class Message():
    def __init__(self, code=None, raw=None, json={}):
        try:
            self.raw = raw
            self.code = code if code != None else raw[:3].strip()
            self.json = json
            
            if raw != None and len(raw) > 3 and json == {}:
                self.json = jsonlib.loads(raw[3:])
            if raw != None and len(raw) < 3:
                if len(raw) < 3:
                    raise Exception("I have received a message that was too small as per the normal message format.\nMessage: %s" % raw)
                
            if self.code == "ERR" and self.json['number'] in [2, 9, 30, 31, 33, 39, 40]:
                handleFatalErrMessage(self)
     
        except Exception as e:
            print("I FAILED TRYING TO CONVERT A RAW MESSAGE")
            print("Message below:")
            print(raw)
            print("Stacktrace:")
            print(traceback.print_exc())
            exit()
            
    def getstring(self):
        return f"{self.code} {jsonlib.dumps(self.json)}"
        
    def __repr__(self):
        return f"<MSG Object [CODE: {self.code}, TEXT: {self.raw}]>"
        
    def __str__(self):
        return f"{self.code} {jsonlib.dumps(self.json)}"
        
def send_out(msg): # Should only be called by bot
    global out_q
    out_q.put(msg)    
            
            
# Test: Does it look like the user tried to type the command 'cmd' properly? 
# This verifies that their message should be: "cmd [parameters]" etc, where cmd can be, say, "!echo" or "!print" or "!slap"
def proper_command(msg, cmd):
        if msg.startswith(cmd):
            if len(msg) == len(cmd):
                return True
            elif msg[len(cmd)] == " ":
                return True
        return False
    
    
######################################################################################### UTILITIES #########################################################################################
        
def recv_thread(connection, chat_q, socket_q):
    for event in persist(connection):
        if event.name == 'text':
            chat_q.put(event)
        else:
            # Socket events. These aren't events sent as f-list's chat protocol. These are websocket messages.
            socket_q.put(event)
            
            
# The bot hosts a socket for LOCAL DATA INPUT that can be utilized via the bot-input.py script provided.
def input_server(input_q):
    # get the hostname
    host = socket.gethostname()
    port = 5000  # initiate port no above 1024

    server_socket = socket.socket()  # get instance
    # look closely. The bind() function takes tuple as argument
    server_socket.bind((host, port))  # bind host address and port together

    # configure how many client the server can listen simultaneously
    server_socket.listen()
    conn, address = server_socket.accept()  # accept new connection
    print("Connection from: " + str(address))
    
    while True:
        # receive data stream. it won't accept data packet greater than 1024 bytes
        try:
            data = conn.recv(1024 * 4).decode()
            if data:
                print("[INPUT SOCKET]: " + str(data))
                send_out(Message(raw=data))
            else:
                conn.close()
                conn, address = server_socket.accept()
                print("Connection from: " + str(address))
            
        except:
            conn.close()
            conn, address = server_socket.accept()
            # Should only be from your localhost IP...
            print("Connection from: " + str(address))
    
# Our thread for sending messages. This makes sure we don't send messages faster than once a second and acts as our output queue.
def send_thread(connection, out_q):
    lastmsg = time.time()
    while True:
        if not out_q.empty():
            if time.time() - lastmsg > 1.05:
                msg = out_q.get()
                
                if msg.json != {}:
                    if "message" in msg.json.keys():
                        if len(msg.json["message"]) >= 4096 and msg.code != "PRI":
                            print("[SEND ERROR]: Did not send message because it was too long.\nMessage text:\n%s[SEND ERROR ABOVE]" % msg.json["message"])
                            continue
                        elif msg.code == "PRI":
                            if len(msg.json["message"]) >= 49000:
                                print("[SEND ERROR]: Did not send message because it was too long.\nMessage text:\n%s[SEND ERROR ABOVE]" % msg.json["message"])
                                continue
                            
                print(f"[SENDING]: {msg}")
                connection.send_text(str(msg))
                lastmsg = time.time()  

# Not for use by others, should only be used internally by the bot dispatcher.
class Module():
    def __init__(self, module, interestFunc, inp_q, moduleTimeout=0, inputs_for_module=(), isPublicFacingCommand=False, cmdname="", cmd_desc=""):
        # inputs_for_module is thusfar unused and merely a thought project for now.
    
        def modwrapper(fn, deathflag, inputs_for_module, inp_q):
            while True:
                try:
                    try:
                        fn(inp_q, *inputs_for_module)
                    except queue.Empty:
                        if deathflag.is_set():
                            exit()
                except Exception as e:
                    errorblock = "############### MODULE ERROR ###############\n############### MODULE ERROR ###############\n############### MODULE ERROR ###############\n############### MODULE ERROR ###############\n"
                    
                    errorstr = "%s\nI have encountered some sort of error in module: %s\n ERROR:\n%s\n\n\nThis module (%s) will exit and not restart again until the bot is restarted for safety.\n\n%s" % \
                                (errorblock, \
                                fn.__module__, \
                                ''.join(traceback.format_exception(None, e, e.__traceback__)), \
                                fn.__module__, \
                                errorblock)
                                
                    print(errorstr)
                    open("error.log", "a").write(errorstr)
                    exit()
    
        self.module = module
        self.deathflag = threading.Event()
        self.moduleThread = threading.Thread(target=modwrapper, args=(module, self.deathflag, inputs_for_module, inp_q))
        self.moduleThread.daemon = True
        
        self.interestFunc = interestFunc
        self.inp_q = inp_q
        self.moduleTimeout = moduleTimeout
        self.isPublicFacingCommand = isPublicFacingCommand
        self.cmdname = cmdname
        self.cmd_desc = cmd_desc
        
        self.startTime = 0
    
    def start(self):
        if not self.is_alive() and not self.deathflag.is_set():
            self.moduleThread.start()
            self.startTime = time.time()
        
    def is_alive(self):
        return self.moduleThread.is_alive()
        
    def __repr__(self):
        return (f"<Module: {self.module.__module__}, moduleTimeout: {self.moduleTimeout}>")
    
    def __str__(self):
        return self.__repr__()

class Dispatcher():
    def __init__(self):
        self.threadpool = []
        self.lasttick = 0
        self.started = False
        
    def register_module(self, module, interestFunc, moduleTimeout=0, inputsForModule=(), isPublicFacingCommand=False, cmdname="", cmd_desc=""):
        inp_q = mp.Queue()
        
        m = Module(module, interestFunc, inp_q, moduleTimeout, inputsForModule, isPublicFacingCommand, cmdname, cmd_desc)
        
        self.threadpool.append(m)
        
    # Boots up all modules loaded
    def start(self):
        if not self.started:
            for module in self.threadpool:
                module.start()
            self.started = True
        
    def send(self, msg):
        if not self.started:
            self.start()
            
        # Take all chat input and throw messages to modules that are interested 
        # For all modules
        for module in list(self.threadpool):
            
            # Remove threads/modules that have died or completed
            if not module.is_alive() or (time.time() - module.startTime > module.moduleTimeout and module.moduleTimeout != 0):
                print("\n\n\n\n\nHEY I am removing: %s" % str(module))
                module.deathflag.set()
                self.threadpool.remove(module)
                print("Currently loaded modules:")
                print(self.threadpool)
                continue
            
            # If the module is interested in a message type, pass it the message.
            try:
                should_send = module.interestFunc(msg)
                if should_send == None:
                    raise Exception("Your predicate function returned None. It should return true or false.")
            except Exception as e: 
                errorblock = "############### MODULE ERROR ###############\n############### MODULE ERROR ###############\n############### MODULE ERROR ###############\n############### MODULE ERROR ###############\n"
                    
                errorstr = "%s\nI have encountered some sort of error in module: %s\n ERROR:\n%s\n\n\nThis module (%s) will exit and not restart again until the bot is restarted for safety.\n\n%s" % \
                            (errorblock, \
                            module.__module__, \
                            ''.join(traceback.format_exception(None, e, e.__traceback__)), \
                            module.__module__, \
                            errorblock)
                print(errorstr)
                open("error.log", "a").write(errorstr)
                module.deathflag.set()
                self.threadpool.remove(module)
                continue
            
            # We successfully got a returned true or false from the predicate, now send it to the handler of the module.
            if should_send:
                module.inp_q.put(msg)

            
        
def main():
    global connection
    global ticket
    global out_q
    
    # Connection
    connection = WebSocket(chat_url)
    connection.connect()
    
    # Queues
    out_q = mp.Queue()
    chat_recv_q = mp.Queue()
    socket_recv_q = mp.Queue()
    input_q = mp.Queue()
    
    # Threads init
    # read thread
    rthread = threading.Thread(target=recv_thread, args=(connection, chat_recv_q, socket_recv_q))
    rthread.daemon = True
    
    # send thread
    sthread = threading.Thread(target=send_thread, args=(connection, out_q))
    sthread.daemon = True
    
    # thread for manual bot input (use bot-input.py) (CLUNKY)
    inputthread = threading.Thread(target=input_server, args=(input_q,))
    inputthread.daemon = True
        
    # Thread starts
    rthread.start()
    sthread.start()
    inputthread.start()
    
    global dispatcher # Allow anything that imports this bot module to access the dispatcher. This means modules can access it AND modify its state. Be careful with that.
    
    dispatcher = Dispatcher()          
                
    # Import all modules in ./Modules/
    from importlib.machinery import SourceFileLoader
    gathered_modules_names = list(map(lambda x: str(x.resolve()), pathlib.Path("./Modules/").rglob("*.py")))
    gathered_modules_names.remove(str(pathlib.Path("./Modules/BotState.py").resolve()))
    print(gathered_modules_names)
    
    imported_modules = []
    
    for item in gathered_modules_names:
        pathobj = pathlib.Path(item)
        modulename, modulepath = pathobj.stem, item
        try:
            imported_modules.append(SourceFileLoader(modulename, modulepath).load_module())
        except Exception as e:
            errorblock = "############### MODULE ERROR ###############\n############### MODULE ERROR ###############\n############### MODULE ERROR ###############\n############### MODULE ERROR ###############\n"
                    
            errorstr = "%s\nI have encountered some sort of error in module when trying to import: %s\n ERROR:\n%s\n\n\nThis module (%s) will !!NOT BE IMPORTED!! for safety.\n\n%s" % \
                        (errorblock, \
                        modulename, \
                        ''.join(traceback.format_exception(None, e, e.__traceback__)), \
                        modulename, \
                        errorblock)
            open("error.log", "a").write(errorstr)


    # Now we verify that they look correct if they imported alright
    
    for item in imported_modules:
        if not hasattr(item, "handler"):
            print("You have imported a module named (\"%s\") from the Modules folder and it does not appear to have a top-level function named \"handler\" defined. Exiting." % (item.__name__))
            exit()
        else:
            def fntype():
                pass
            if type(fntype) != type(item.handler):
                print("It appears you have something named \"handler\" in your module named \"%s\", but it is NOT a function defined as 'def func(msg_pipe[,args...]):...'. Please check the docs." % item.__name__)
                exit()
                
        if not hasattr(item, "predicate"):
            print("You have imported a module named (\"%s\") from the Modules folder and it does not appear to have a top-level function named \"predicate\" defined. Exiting." % (item.__name__))
            exit()
        else:
            if type(fntype) != type(item.predicate):
                print("It appears you have something named \"predicate\" in your module named \"%s\", but it is NOT a function defined as 'def func(msg_pipe):...'. Please check the docs." % item.__name__)
                exit()
                
        if not hasattr(item, "HasHelpInfo"):
            print("You must specify if your module (\"%s\") has help info via setting the variable \"HasHelpInfo\" to True or False in your module's global scope." % item.__name__)
            exit()
            
        if item.HasHelpInfo:
            if not hasattr(item, "command_name"):
                print("You have imported a module named (\"%s\") from the Modules folder, and have specified that it has help info via the HasHelpInfo flag.\nYou need to still specify a global variable named \"command_name\" in the module in this case!" % (item.__name__))
                exit()
            if not hasattr(item, "command_description"):
                print("You have imported a module named (\"%s\") from the Modules folder, and have specified that it has help info via the HasHelpInfo flag.\nYou need to still specify a global variable named \"command_description\" in the module in this case!\n\nNOTE: You may set command_description to an empty string, in which case the bot will report that there is no description for the command." % (item.__name__))
                exit()
            
    for item in imported_modules:
        if item.HasHelpInfo:
            dispatcher.register_module(item.handler, item.predicate, False, (), item.HasHelpInfo, item.command_name, item.command_description)
        else:
            dispatcher.register_module(item.handler, item.predicate, False, (), item.HasHelpInfo)
    
    while True:
        # Socket Queue
        if not socket_recv_q.empty():
            event = socket_recv_q.get()
            if event.name not in ["poll", "pong"]:
                print(f"[SOCKET MESSAGE]: {event}")
            
            # Send login code to chat once socket is ready.
            if event.name == 'ready':
                send_out(Message(code="IDN", json={"method":"ticket", "account":username, "ticket": getTicket(), "character":botname, "cname": cname, "cversion": cversion}))
            
        # Chat Queue
        if not chat_recv_q.empty():
            msg = chat_recv_q.get()
            msg = Message(raw=msg.text)
            dispatcher.send(msg)
            
# entry point
if __name__ == '__main__':
    global ticket
    global tickettime
    global ticketlock
    
    # init globals
    ticket = ""
    tickettime = time.time()
    ticketlock = Lock()
    
    ticket = getTicket()
    
    main()
    
    
    
    