"""Main module."""
from chattool import Chat, debug_log
import asyncio
from argparse import ArgumentParser
import askchat
VERSION = askchat.__version__

# print the response in a typewriter way
async def show_resp(chat):
    async for resp in chat.async_stream_responses():
        for char in resp.delta_content:
            print(char, end='', flush=True)
            await asyncio.sleep(0.015)

def ask():
    """Interact with ChatGPT in terminal via chattool"""
    # parse arguments
    parser = ArgumentParser()
    parser.add_argument('message', type=str, help='User message')
    args = parser.parse_args()
    msg = args.message
    
    # call
    chat = Chat(msg)
    asyncio.run(show_resp(chat))

def main():
    """Interact with ChatGPT in terminal via chattool"""
    # parse arguments
    parser = ArgumentParser()
    ## use nargs='?' to make message optional
    parser.add_argument('message', help='User message', default='', nargs='?')
    parser.add_argument('-v', '--version', action='version', version=VERSION)
    parser.add_argument('--debug', action='store_true', help='Print debug log')
    parser.add_argument('--valid-models', action='store_true', help='Print valid models')
    parser.add_argument('-m', '--model', default=None, help='Model name')
    args = parser.parse_args()
    # show debug log
    if args.debug:
        debug_log()
        return
    # show valid models
    if args.valid_models:
        print('Valid models: ')
        print(Chat().get_valid_models())
        return
    # get message and model
    model, msg = args.model, args.message
    assert len(msg.strip()), 'Please specify message'
    # call
    chat = Chat(msg, model=model)
    asyncio.run(show_resp(chat))