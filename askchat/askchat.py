"""Main module."""

import click, asyncio, askchat
from pathlib import Path
from pprint import pprint
from dotenv import load_dotenv, set_key
import asyncio, os, uuid, shutil, json
from chattool import Chat, debug_log, load_envs
from pathlib import Path
from .ask import show_resp

# Version and Config Path
VERSION = askchat.__version__
CONFIG_PATH = Path.home() / ".askchat"
CONFIG_FILE = CONFIG_PATH / ".env"
LAST_CHAT_FILE = CONFIG_PATH / "_last_chat.json"

def setup():
    """Application setup: Ensure that necessary folders and files exist."""
    os.makedirs(CONFIG_PATH, exist_ok=True)
    if not os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'w') as cf:
            cf.write("# Initial configuration\n")
    # if not os.path.exists(LAST_CHAT_FILE):
    #     with open(LAST_CHAT_FILE, 'w') as lcf:
    #         lcf.write('{"index": 0, "chat_log": []}')

def print_callback(ctx, param, value):
    print("无参数，回调")
    if value is None:
        return "_last_chat"  # default value
    return value

def generate_config():
    pass

def load_config():
    pass

@click.group()
def cli():
    """A CLI for interacting with ChatGPT with advanced options."""
    pass

@cli.command()
@click.argument('message', nargs=-1)
@click.option('-m', '--model', default=None, help='Model name')
@click.option('-b', '--base-url', default=None, help='Base URL of the API (without suffix `/v1`)')
@click.option('--api-base', default=None, help='Base URL of the API (with suffix `/v1`)')
@click.option('-a', '--api-key', default=None, help='OpenAI API key')
# Chat with history
@click.option('-c', is_flag=True, help='Continue the last conversation')
@click.option('-r', '--regenerate', is_flag=True, help='Regenerate the last conversation')
@click.option('-s', '--save', default=None, help='Save the conversation to a file')
@click.option('-l', '--load', default=None, help='Load the conversation from a file')
@click.option('-p', '--print', is_flag=True, help='Print the last conversation or a specific conversation')
@click.option('-d', '--delete', default=None, help='Delete the conversation from a file')
@click.option('--list', is_flag=True, help='List all the conversation files')
# Other options
@click.option('--generate-config', is_flag=True, help='Generate a configuration file by environment table')
@click.option('--debug', is_flag=True, help='Print debug log')
@click.option('--valid-models', is_flag=True, help='Print valid models that contain "gpt" in their names')
@click.option('--all-valid-models', is_flag=True, help='Print all valid models')
@click.option('-v', '--version', is_flag=True, help='Print the version')
def askchat( message, model, base_url, api_base, api_key
           , c, regenerate, save, load, print, delete, list
           , generate_config, debug, valid_models, all_valid_models, version):
    """Interact with ChatGPT in terminal via chattool"""
    setup()
    message_text = ' '.join(message).strip()
    # generate config file
    if generate_config:
        return generate_config()
    # set values for the environment variables
    ## 1. read from config file `~/.askchat/.env`
    # load_config()
    ## 2. read from command line
    if api_key:
        os.environ['OPENAI_API_KEY'] = api_key
    if base_url:
        os.environ['OPENAI_API_BASE_URL'] = base_url
    if api_base:
        os.environ['OPENAI_API_BASE'] = api_base
    if model:
        os.environ['OPENAI_API_MODEL'] = model
    # update environment variables of chattool
    load_envs()
    # show debug log
    if debug:
        return debug_log()
    # show valid models
    if valid_models:
        click.echo('Valid models that contain "gpt" in their names:')
        click.echo(pprint(Chat().get_valid_models()))
        return
    if all_valid_models:
        click.echo('All valid models:')
        click.echo(pprint(Chat().get_valid_models(gpt_only=False)))
        return
    # Handle chat history operations
    if load:
        try:
            shutil.copyfile(CONFIG_PATH / f"{load}.json", LAST_CHAT_FILE)
            click.echo(f"Loaded conversation from {CONFIG_PATH}/{load}.json")
        except FileNotFoundError:
            click.echo(f"The specified conversation {load} does not exist." +\
                       "Please check the chat list with `--list` option.")
        return
    if save:
        try:
            shutil.copyfile(LAST_CHAT_FILE, CONFIG_PATH / f"{save}.json")
            click.echo(f"Saved conversation to {CONFIG_PATH}/{save}.json")
        except FileNotFoundError:
            click.echo("No last conversation to save.")
        return
    if delete:
        try:
            os.remove(CONFIG_PATH / f"{delete}.json")
            click.echo(f"Deleted conversation at {CONFIG_PATH}/{delete}.json")
        except FileNotFoundError:
            click.echo(f"The specified conversation {CONFIG_PATH}/{delete}.json does not exist.")
        return
    if list:
        click.echo("All conversation files:")
        for file in CONFIG_PATH.glob("*.json"):
            if not file.name.startswith("_"):
                click.echo(f" - {file.stem}")
        return
    if print:
        fname = message_text if message_text else '_last_chat'
        fname = f"{CONFIG_PATH}/{fname}.json"
        try:
            Chat().load(fname).print_log()
        except FileNotFoundError:
            click.echo(f"The specified conversation {fname} does not exist.")
        return
    # Handle version option
    if version:
        click.echo(f"askchat version: {VERSION}")
        return
    # Main chat
    chat = Chat()
    if c or regenerate: # Load last chat if -c or -r is used
        try:
            chat = Chat.load(LAST_CHAT_FILE)
        except FileNotFoundError:
            click.echo("No last conversation found. Starting a new conversation.")
            return
    if regenerate:
        if len(chat) < 2:
            click.echo("You should have at least two messages in the conversation")
            return
        chat.pop()
    else:
        if not message_text:
            click.echo("Please specify message!")
            return
        chat.user(message_text)
    # Simulate chat response
    chat.assistant(asyncio.run(show_resp(chat)))
    chat.save(LAST_CHAT_FILE, mode='w')

if __name__ == '__main__':
    cli()