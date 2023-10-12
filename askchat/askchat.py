"""Main module."""
from chattool import Chat
import asyncio
from argparse import ArgumentParser

def ask():
    """Interact with ChatGPT in terminal via chattool"""
    # parse arguments
    parser = ArgumentParser()
    parser.add_argument('message', type=str, help='User message')
    args = parser.parse_args()
    msg = args.message

    # print the response in a typewriter way
    async def show_resp(chat):
        async for resp in chat.async_stream_responses():
            for char in resp.delta_content:
                print(char, end='', flush=True)
                await asyncio.sleep(0.015)
    
    # call
    chat = Chat(msg)
    asyncio.run(show_resp(chat))