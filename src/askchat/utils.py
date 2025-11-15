import os
from dotenv import set_key
from chattool import create_env_file, Chat

# common functions
async def show_resp(chat:Chat, **options):
    msg = ''
    async for resp in chat.async_get_response_stream(**options):
        print(resp.delta_content, end='', flush=True)
        msg += resp.delta_content
        # await asyncio.sleep(0.01)
    if not msg.endswith('\n'):
        print() # add a newline if the message doesn't end with one
    return msg

def set_keys(config_file, keys):
    """Set multiple keys in the config file."""
    for key, value in keys.items():
        if value:
            set_key(config_file, key, value)

def initialize_config(config_file:str):
    """Initialize the config file with the current environment variables."""
    create_env_file(config_file)
    set_keys(config_file, {
        "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY"),
        "OPENAI_API_MODEL": os.getenv("OPENAI_API_MODEL"),
        "OPENAI_API_BASE_URL": os.getenv("OPENAI_API_BASE_URL"),
        "OPENAI_API_BASE": os.getenv("OPENAI_API_BASE"),
    })

def write_config(config_file, api_key, model, base_url, api_base, overwrite=False):
    """Write the environment variables to a config file."""
    if overwrite or not config_file.exists():
        create_env_file(config_file)
    set_keys(config_file, {
        "OPENAI_API_KEY": api_key,
        "OPENAI_API_MODEL": model,
        "OPENAI_API_BASE_URL": base_url,
        "OPENAI_API_BASE": api_base,
    })