"""Main module."""

import click, asyncio, askchat, chattool
from pathlib import Path
from pprint import pprint
from dotenv import load_dotenv
import asyncio, os, shutil
from chattool import Chat, debug_log
from pathlib import Path
from askchat import (
      show_resp, write_config, initialize_config
    , ENV_PATH, MAIN_ENV_PATH
    , CONFIG_PATH, CONFIG_FILE
    , EnvNameCompletionType, ChatFileCompletionType
)

# Version and Config Path
VERSION = askchat.__version__
LAST_CHAT_FILE = CONFIG_PATH / "_last_chat.json"

help_message = """Interact with ChatGPT in terminal via chattool.

To enable autocompletion, add the following line to your shell configuration file (e.g., .bashrc, .zshrc):

For zsh users: eval "$(_ASKCHAT_COMPLETE=zsh_source askchat)"

For bash users: eval "$(_ASKCHAT_COMPLETE=bash_source askchat)\""""

def setup():
    """Application setup: Ensure that necessary folders and files exist."""
    os.makedirs(CONFIG_PATH, exist_ok=True)
    if os.path.exists(CONFIG_FILE):
        load_dotenv(CONFIG_FILE, override=True)
    chattool.load_envs()

# callback functions for general options
def generate_config_callback(ctx, param, value):
    """Generate a configuration file by environment table."""
    if not value: return
    # save the config file
    if os.path.exists(CONFIG_FILE):
        click.confirm(f"Overwrite the existing configuration file {CONFIG_FILE}?", abort=True)
    initialize_config(CONFIG_FILE)
    print("Created config file at", CONFIG_FILE)
    ctx.exit()

def debug_log_callback(ctx, param, value):
    if not value: return
    setup()
    debug_log()
    ctx.exit()

def valid_models_callback(ctx, param, value):
    if not value: return
    setup()
    click.echo('Valid models that contain "gpt" in their names:')
    click.echo(pprint(Chat().get_valid_models()))
    ctx.exit()

def all_valid_models_callback(ctx, param, value):
    if not value: return
    setup()
    click.echo('All valid models:')
    click.echo(pprint(Chat().get_valid_models(gpt_only=False)))
    ctx.exit()

def version_callback(ctx, param, value):
    if not value:
        return
    click.echo(f"askchat version: {VERSION}")
    ctx.exit()

# callback functions for handling chat history
def save_chat_callback(ctx, param, value):
    if not value:
        return
    try:
        shutil.copyfile(LAST_CHAT_FILE, CONFIG_PATH / f"{value}.json")
        click.echo(f"Saved conversation to {CONFIG_PATH}/{value}.json")
    except FileNotFoundError:
        click.echo("No last conversation to save.")
    ctx.exit()

def delete_chat_callback(ctx, param, value):
    if not value:
        return
    try:
        os.remove(CONFIG_PATH / f"{value}.json")
        click.echo(f"Deleted conversation at {CONFIG_PATH}/{value}.json")
    except FileNotFoundError:
        click.echo(f"The specified conversation {CONFIG_PATH}/{value}.json does not exist.")
    ctx.exit()

def list_chats_callback(ctx, param, value):
    if not value:
        return
    click.echo("All conversation files:")
    for file in CONFIG_PATH.glob("*.json"):
        if not file.name.startswith("_"):
            click.echo(f" - {file.stem}")
    ctx.exit()

def load_chat_callback(ctx, param, value):
    if not value: return
    try:
        shutil.copyfile(CONFIG_PATH / f"{value}.json", LAST_CHAT_FILE)
        click.echo(f"Loaded conversation from {CONFIG_PATH}/{value}.json")
    except FileNotFoundError:
        click.echo(f"The specified conversation {value} does not exist." +\
                   "Please check the chat list with `--list` option.")
    ctx.exit()
# callback function for --use-env option
def use_env_callback(ctx, param, value):
    if not value:
        return
    env_file = ENV_PATH / f"{value}.env"
    if env_file.exists():
        content = env_file.read_text()
        MAIN_ENV_PATH.write_text(content)
        setup()
        click.echo(f"Environment '{value}' activated.")
    else:
        raise click.BadParameter(f"Environment file {env_file} does not exist.")
    return value

@click.group()
def cli():
    """A CLI for interacting with ChatGPT with advanced options."""
    pass

@cli.command(help=help_message)
@click.argument('message', nargs=-1)
@click.option('-m', '--model', default=None, help='Model name')
@click.option('-b', '--base-url', default=None, help='Base URL of the API (without suffix `/v1`)')
@click.option('--api-base', default=None, help='Base URL of the API (with suffix `/v1`)')
@click.option('-a', '--api-key', default=None, help='OpenAI API key')
@click.option('-u', '--use-env', type=EnvNameCompletionType(), help='Use environment variables from the `~/.askchat/envs`', callback=use_env_callback, expose_value=True)
# Chat with history
@click.option('-c', is_flag=True, help='Continue the last conversation')
@click.option('-r', '--regenerate', is_flag=True, help='Regenerate the last conversation')
@click.option('-l', '--load', default=None, type=ChatFileCompletionType(), callback=load_chat_callback, expose_value=False, help='Load a conversation from a file')
# Handling chat history
@click.option('-p', is_flag=True, help='Print the last conversation or a specific conversation')
@click.option('-s', '--save', callback=save_chat_callback, expose_value=False, help='Save the conversation to a file')
@click.option('-d', '--delete', type=ChatFileCompletionType(), callback=delete_chat_callback, expose_value=False, help='Delete the conversation from a file')
@click.option('--list', is_flag=True, callback=list_chats_callback, expose_value=False, help='List all the conversation files')
# Other options
@click.option('--generate-config', is_flag=True, callback=generate_config_callback, expose_value=False, help='Generate a configuration file by environment table')
@click.option('--debug', is_flag=True, callback=debug_log_callback, expose_value=False, help='Print debug log')
@click.option('--valid-models', is_flag=True, callback=valid_models_callback, expose_value=False, help='Print valid models that contain "gpt" in their names')
@click.option('--all-valid-models', is_flag=True, callback=all_valid_models_callback, expose_value=False, help='Print all valid models')
@click.option('--print-curl', is_flag=True, help='Print the curl command for the request')
@click.option('-v', '--version', is_flag=True, callback=version_callback, expose_value=False, help='Print the version')
@click.option('-o', '--option', multiple=True, type=(str, str), help='Additional options for show_resp in the form of key=value')
def main( message, model, base_url, api_base, api_key, use_env
        , c, regenerate, p, option, print_curl):
    """Interact with ChatGPT in terminal via chattool"""
    setup()
    message_text = ' '.join(message).strip()
    if use_env and not message_text: return
    # set values for the environment variables
    if api_key:
        os.environ['OPENAI_API_KEY'] = api_key
    if base_url:
        os.environ['OPENAI_API_BASE_URL'] = base_url
    if api_base:
        os.environ['OPENAI_API_BASE'] = api_base
    if model:
        os.environ['OPENAI_API_MODEL'] = model
    chattool.load_envs() # update the environment variables in chattool
    # print chat messages
    if p:
        fname = message_text if message_text else '_last_chat'
        fname = f"{CONFIG_PATH}/{fname}.json"
        try:
            Chat().load(fname).print_log()
        except FileNotFoundError:
            click.echo(f"The specified conversation {fname} does not exist.")
        return
    # handling chat history | Four cases: regenerate, load, continue, default
    chat = Chat()
    if regenerate:
        try:
            chat = Chat.load(LAST_CHAT_FILE)
        except FileNotFoundError:
            click.echo("No last conversation found. Starting a new conversation.")
            return
        if len(chat) < 2:
            click.echo("You should have at least two messages in the conversation")
            return
        chat.pop()
    elif c: # continue the last conversation
        if not message_text:
            click.echo("Please specify message!")
            return
        try:
            chat = Chat.load(LAST_CHAT_FILE)
        except FileNotFoundError:
            click.echo("No last conversation found. Starting a new conversation.")
            return
        chat.user(message_text)
    else:
        if not message_text:
            click.echo("Please specify message!")
            return
        chat.user(message_text)
    # additinal options
    if option:
        option = dict(option)
        ints = ['max_tokens', 'n', 'top_logprobs', 'seed']
        floats = ['temperature', 'presence_penalty', 'frequency_penalty', 'top_p']
        for key, value in option.items():
            if key in ints:
                option[key] = int(value)
            elif key in floats:
                option[key] = float(value)
    else:
        option = {}
    if option.get('stream') in ['false', 0]:
        option['stream'] = False
    else:
        option['stream'] = True
    if print_curl:
        chat.print_curl(**option)
        return 
    # Add chat responses
    if not option['stream']:
        chat.getresponse(**option)
        for text in chat.last_message:
            print(text, end='', flush=True)
    else:
        chat.assistant(asyncio.run(show_resp(chat, **dict(option))))
        
    chat.save(LAST_CHAT_FILE, mode='w')

if __name__ == '__main__':
    cli()