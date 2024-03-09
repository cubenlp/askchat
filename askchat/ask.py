import click
import asyncio
from chattool import Chat

async def show_resp(chat):
    msg = ''
    async for char in chat.async_stream_responses(textonly=True):
        print(char, end='', flush=True)
        msg += char
        await asyncio.sleep(0.01)
    return msg

@click.command()
@click.argument('message', nargs=-1, required=True)
def ask(message):
    """Send a message to ChatGPT and display the response."""
    message = ' '.join(message).strip()
    if not message:
        click.echo("Cannot send an empty message")
        return
    chat = Chat(message)
    asyncio.run(show_resp(chat))

if __name__ == '__main__':
    ask()
