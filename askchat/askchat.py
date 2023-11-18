"""Main module."""
from chattool import Chat, debug_log
import asyncio
from argparse import ArgumentParser
import askchat
from pprint import pprint
VERSION = askchat.__version__

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
    # get message and model
    model, msg = args.model, args.message
    if isinstance(msg, list):
        msg = ' '.join(msg)
    assert len(msg.strip()), 'Please specify message'
    # call
    chat = Chat(msg, model=model)
    asyncio.run(show_resp(chat))