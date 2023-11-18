"""Main module."""
from chattool import Chat, debug_log
import asyncio, os, uuid
from argparse import ArgumentParser
import askchat
from pprint import pprint
VERSION = askchat.__version__
CONFIG_FILE = os.path.expanduser("~/.askrc")

# print the response in a typewriter way
async def show_resp(chat):
    async for char in chat.async_stream_responses(textonly=True):
        print(char, end='', flush=True)

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
    ## use nargs='?' to make message optional
    parser.add_argument('message', help='User message', default='', nargs='*')
    parser.add_argument('-v', '--version', action='version', version=VERSION)
    parser.add_argument('--debug', action='store_true', help='Print debug log')
    parser.add_argument('--valid-models', action='store_true', help='Print valid models that contain "gpt" in their names')
    parser.add_argument('--all-valid-models', action='store_true', help='Print all valid models')
    parser.add_argument('-m', '--model', default=None, help='Model name')
    parser.add_argument('--base-url', default=None, help='base url of the api(without suffix `/v1`)')
    parser.add_argument("--api-key", default=None, help="API key")
    parser.add_argument('--generate-config', action="store_true", help="Generate a configuration file by environment table.")
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
    if args.generate_config is not None:
        api_key = os.environ.get("OPENAI_API_KEY", "")
        base_url = os.environ.get("OPENAI_API_BASE_URL", "")
        model = os.environ.get("OPENAI_API_MODEL", "")
        if os.path.exists(CONFIG_FILE):
            # create a temporary file
            os.makedirs("/tmp", exist_ok=True)
            tmp_file = os.path.join("/tmp", str(uuid.uuid4())[:8] + ".askrc")
            # move the old config file to a temporary file
            os.rename(CONFIG_FILE, tmp_file)
            print(f"Moved old config file to {tmp_file}")
        with open(CONFIG_FILE, "w") as f:
            # description for the config file
            f.write("#!/bin/bash\n" +\
                    "# Description: This is a configuration file for askchat.\n" +\
                    "# Author: Rex Wang\n" +\
                    "# Current version: " + VERSION + "\n\n")
            # write the environment table
            f.write("# Your API key\n")
            f.write(f"OPENAI_API_KEY={api_key}\n\n")
            f.write("# The base url of the API (without suffix /v1)\n")
            f.write(f"OPENAI_API_BASE_URL={base_url}\n\n")
            f.write("# The model name. You can use `askchat --all-valid-models` to see the valid models.\n")
            f.write(f"OPENAI_API_MODEL={model}\n\n")
            print("Created config file at", CONFIG_FILE)
        return

    # get message, model, and base url
    msg = args.message
    if isinstance(msg, list):
        msg = ' '.join(msg)
    assert len(msg.strip()), 'Please specify message'
    # read para from config or args
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE) as f:
            lines = f.readlines()
        for line in lines:
            if line.startswith("OPENAI_API_KEY="):
                api_key = line.split("=")[-1].strip()
            elif line.startswith("OPENAI_API_BASE_URL="):
                base_url = line.split("=")[-1].strip()
            elif line.startswith("OPENAI_API_MODEL="):
                model = line.split("=")[-1].strip()
    api_key = args.api_key if hasattr(args, "api_key") else api_key
    base_url = args.base_url if hasattr(args, "base_url") else base_url
    model = args.model if hasattr(args, "model") else model
    # call the function
    chat = Chat(msg, model=model, base_url=base_url, api_key=api_key)
    asyncio.run(show_resp(chat))