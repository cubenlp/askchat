"""Top-level package for askchat."""

__author__ = """Rex Wang"""
__email__ = '1073853456@qq.com'
__version__ = '1.2.1'

import asyncio
from pathlib import Path
import click
from dotenv import set_key
import os

# Main environment file
CONFIG_PATH = Path.home() / ".askchat"
CONFIG_FILE = CONFIG_PATH / ".env"
MAIN_ENV_PATH = Path.home() / '.askchat' / '.env'
ENV_PATH = Path.home() / '.askchat' / 'envs'

raw_env_text = f"""# Description: Env file for askchat.
# Current version: {__version__}

# The base url of the API (with suffix /v1)
# This will override OPENAI_API_BASE_URL if both are set.
OPENAI_API_BASE=''

# The base url of the API (without suffix /v1)
OPENAI_API_BASE_URL=''

# Your API key
OPENAI_API_KEY=''

# The default model name
# You can use `askchat --all-valid-models` to see supported models
OPENAI_API_MODEL=''
"""

# Autocompletion
# environment name completion
class EnvNameCompletionType(click.ParamType):
    name = "envname"
    def shell_complete(self, ctx, param, incomplete):
        return [
            click.shell_completion.CompletionItem(path.stem) for path in ENV_PATH.glob(f"{incomplete}*.env")
        ]
# chat file completion
class ChatFileCompletionType(click.ParamType):
    name = "chatfile"
    def shell_complete(self, ctx, param, incomplete):
        return [
            click.shell_completion.CompletionItem(path.stem) for path in CONFIG_PATH.glob(f"{incomplete}*.json")
            if not path.name.startswith("_")
        ]

# common functions
async def show_resp(chat, **options):
    msg = ''
    async for char in chat.async_stream_responses(textonly=True, **options):
        print(char, end='', flush=True)
        msg += char
        # await asyncio.sleep(0.01)
    if not msg.endswith('\n'):
        print() # add a newline if the message doesn't end with one
    return msg

def set_keys(config_file, keys):
    """Set multiple keys in the config file."""
    for key, value in keys.items():
        if value:
            set_key(config_file, key, value)

def create_empty_config(config_file:str):
    """Empty config file."""
    if not CONFIG_PATH.exists():
        CONFIG_PATH.mkdir(parents=True)
    with open(config_file, "w") as f:
        f.write(raw_env_text)

def initialize_config(config_file:str):
    """Initialize the config file with the current environment variables."""
    create_empty_config(config_file)
    set_keys(config_file, {
        "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY"),
        "OPENAI_API_MODEL": os.getenv("OPENAI_API_MODEL"),
        "OPENAI_API_BASE_URL": os.getenv("OPENAI_API_BASE_URL"),
        "OPENAI_API_BASE": os.getenv("OPENAI_API_BASE"),
    })

def write_config(config_file, api_key, model, base_url, api_base, overwrite=False):
    """Write the environment variables to a config file."""
    if overwrite or not config_file.exists():
        create_empty_config(config_file)
    set_keys(config_file, {
        "OPENAI_API_KEY": api_key,
        "OPENAI_API_MODEL": model,
        "OPENAI_API_BASE_URL": base_url,
        "OPENAI_API_BASE": api_base,
    })