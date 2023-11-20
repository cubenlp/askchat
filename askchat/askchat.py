"""Main module."""

from argparse import ArgumentParser
from pprint import pprint
from dotenv import load_dotenv, set_key
import asyncio, os, uuid
import askchat

VERSION = askchat.__version__
CONFIG_PATH = os.path.expanduser("~/.askchat")
CONFIG_FILE = os.path.expanduser("~/.askchat/.env")
## read para from config file
if os.path.exists(CONFIG_FILE):
    load_dotenv(CONFIG_FILE, override=True)

# load chattool after update the config
from chattool import Chat, debug_log

# print the response in a typewriter way
async def show_resp(chat, delay=0.01):
    async for char in chat.async_stream_responses(textonly=True):
        print(char, end='', flush=True)
        await asyncio.sleep(delay)

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
    ## other options
    parser.add_argument('--debug', action='store_true', help='Print debug log')
    parser.add_argument('--valid-models', action='store_true', help='Print valid models that contain "gpt" in their names')
    parser.add_argument('--all-valid-models', action='store_true', help='Print all valid models')
    parser.add_argument('--generate-config', action="store_true", help="Generate a configuration file by environment table")
    parser.add_argument('-v', '--version', action='version', version=VERSION)
    args = parser.parse_args()
    
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
            os.rename(CONFIG_FILE, tmp_file)
            print(f"Moved old config file to {tmp_file}")
        # save the config file
        os.makedirs(CONFIG_PATH, exist_ok=True)
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

    # get message, model, and base url
    msg = args.message
    if isinstance(msg, list):
        msg = ' '.join(msg)
    assert len(msg.strip()), 'Please specify message'
    
    # call the function
    chat = Chat(msg, model=args.model, base_url=args.base_url, api_key=args.api_key)
    asyncio.run(show_resp(chat))