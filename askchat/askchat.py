"""Main module."""

from argparse import ArgumentParser
from pprint import pprint
from dotenv import load_dotenv, set_key
import asyncio, os, uuid, json, shutil
import askchat

VERSION = askchat.__version__
CONFIG_PATH = os.path.expanduser("~/.askchat")
CONFIG_FILE = os.path.expanduser("~/.askchat/.env")
LAST_CHAT_FILE = os.path.expanduser("~/.askchat/_last_chat.json")
os.makedirs(CONFIG_PATH, exist_ok=True)
## read para from config file
if os.path.exists(CONFIG_FILE):
    load_dotenv(CONFIG_FILE, override=True)

# load chattool after update the config
from chattool import Chat, debug_log

# print the response in a typewriter way
async def show_resp(chat, delay=0.01):
    msg = ''
    async for char in chat.async_stream_responses(textonly=True):
        print(char, end='', flush=True)
        msg += char
        await asyncio.sleep(delay)
    return msg

def ask():
    """Interact with ChatGPT in terminal via chattool"""
    # parse arguments
    parser = ArgumentParser()
    parser.add_argument('message', help='User message', default='', nargs='*')
    args = parser.parse_args()
    msg = args.message
    if isinstance(msg, list):
        msg = ' '.join(msg)
    assert len(msg.strip()), 'Please specify message'
    # call
    chat = Chat(msg)
    asyncio.run(show_resp(chat))

def main():
    """Interact with ChatGPT in terminal via chattool"""
    # parse arguments
    parser = ArgumentParser()
    ## arguments for chat message
    parser.add_argument('message', help='User message', default='', nargs='*')
    parser.add_argument('-m', '--model', default=None, help='Model name')
    parser.add_argument('--base-url', default=None, help='base url of the api(without suffix `/v1`)')
    parser.add_argument("--api-key", default=None, help="API key")
    ## Chat with history
    parser.add_argument('-c', action='store_true', help='Continue the last conversation')
    parser.add_argument('-r', action='store_true', help='Regenerate the last conversation')
    parser.add_argument('-s', "--save", default=None, help="Save the conversation to a file")
    parser.add_argument("-l", "--load", default=None, help="Load the conversation from a file")
    parser.add_argument("-p", "--print", default=None, nargs='*', help="Print the conversation from " +\
                        "a file or the last conversation if no file is specified")
    parser.add_argument("-d", "--delete", default=None, help="Delete the conversation from a file")
    parser.add_argument("--list", action="store_true", help="List all the conversation files")
    ## other options
    parser.add_argument('--debug', action='store_true', help='Print debug log')
    parser.add_argument('--valid-models', action='store_true', help='Print valid models that contain "gpt" in their names')
    parser.add_argument('--all-valid-models', action='store_true', help='Print all valid models')
    parser.add_argument('--generate-config', action="store_true", help="Generate a configuration file by environment table")
    parser.add_argument('-v', '--version', action='version', version=VERSION)
    args = parser.parse_args()
    
    # set values
    if args.api_key:
        os.environ['OPENAI_API_KEY'] = args.api_key
    if args.base_url:
        os.environ['OPENAI_API_BASE_URL'] = args.base_url
    if args.model:
        os.environ['OPENAI_API_MODEL'] = args.model
    # show debug log
    if args.debug:
        debug_log()
        return
    
    # show valid models
    if args.valid_models:
        print('Valid models that contain "gpt" in their names:')
        pprint(Chat().get_valid_models())
        return
    if args.all_valid_models:
        print('All valid models:')
        pprint(Chat().get_valid_models(gpt_only=False))
        return
    
    # generate config file
    if args.generate_config:
        api_key = os.environ.get("OPENAI_API_KEY")
        base_url = os.environ.get("OPENAI_API_BASE_URL")
        model = os.environ.get("OPENAI_API_MODEL")
        # move the old config file to a temporary file
        if os.path.exists(CONFIG_FILE):
            # create a temporary file
            os.makedirs("/tmp", exist_ok=True)
            tmp_file = os.path.join("/tmp", str(uuid.uuid4())[:8] + ".askchat.env")
            # move the old config file to a temporary file
            shutil.move(CONFIG_FILE, tmp_file)
            print(f"Moved old config file to {tmp_file}")
        # save the config file
        with open(CONFIG_FILE, "w") as f:
            # description for the config file
            f.write("#!/bin/bash\n" +\
                    "# Description: Env file for askchat.\n" +\
                    "# Current version: " + VERSION + "\n\n" +\
                    "# The base url of the API (without suffix /v1)\n" +\
                    "OPENAI_API_BASE_URL=\n\n" +\
                    "# Your API key\n" +\
                    "OPENAI_API_KEY=\n\n" +\
                    "# The model name\n" +\
                    "# You can use `askchat --all-valid-models` to see the valid models\n" +\
                    "OPENAI_API_MODEL=\n\n")
        # write the environment table
        if api_key: set_key(CONFIG_FILE, "OPENAI_API_KEY", api_key)
        if base_url: set_key(CONFIG_FILE, "OPENAI_API_BASE_URL", base_url)
        if model: set_key(CONFIG_FILE, "OPENAI_API_MODEL", model)
        print("Created config file at", CONFIG_FILE)
        return

    # deal with chat history
    call_history = False
    ## load chat
    if args.load is not None:
        new_file = os.path.join(CONFIG_PATH, args.load) + ".json"
        shutil.copyfile(new_file, LAST_CHAT_FILE)
        print("Loaded conversation from", new_file)
        call_history = True
    ## save chat
    if args.save is not None:
        new_file = os.path.join(CONFIG_PATH, args.save) + ".json"
        shutil.copyfile(LAST_CHAT_FILE, new_file)
        print("Saved conversation to", new_file)
        call_history = True
    ## delete chat
    if args.delete is not None:
        new_file = os.path.join(CONFIG_PATH, args.delete) + ".json"
        if os.path.exists(new_file):
            os.remove(new_file)
            print("Deleted conversation at", new_file)
        else:
            print("No such file", new_file)
        call_history = True
    ## list chat
    if args.list:
        print("All conversation files:")
        for file in os.listdir(CONFIG_PATH):
            if not file.startswith("_") and file.endswith(".json"):
                print(" -", file[:-5])
        call_history = True
    ## print chat
    if args.print is not None:
        names = args.print
        assert len(names) <= 1, "Only one file can be specified"
        new_file = os.path.join(CONFIG_PATH, names[0]) + ".json" if len(names) else LAST_CHAT_FILE
        chat = Chat.load(new_file)
        chat.print_log()
        call_history = True
    if call_history: return
    # Initial message
    msg = args.message
    if isinstance(msg, list):
        msg = ' '.join(msg).strip()
    chat = Chat(msg)
    if os.path.exists(LAST_CHAT_FILE):
        if args.c:
            chat = Chat.load(LAST_CHAT_FILE)
            chat.user(msg)
        elif args.r:
            # pop out the last two messages
            chat = Chat.load(LAST_CHAT_FILE)
            assert len(chat) > 1, "You should have at least two messages in the conversation"
            chat.pop()
            if len(msg) != 0: # not empty message
                chat.pop()
                chat.user(msg)
            # if msg is empty, regenerate the last message
    assert len(chat) > 0 and len(chat.last_message) > 0, "Please specify message!"
    # call the function
    newmsg = asyncio.run(show_resp(chat))
    chat.assistant(newmsg)
    chat.save(LAST_CHAT_FILE, mode='w')