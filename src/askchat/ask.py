import click
import asyncio
from chattool import Chat
from askchat import show_resp

@click.command()
@click.argument('message', nargs=-1, required=True)
def main(message):
    """Send a message to ChatGPT and display the response."""
    message = ' '.join(message).strip()
    if not message:
        click.echo("Cannot send an empty message")
        return
    chat = Chat(message)
    asyncio.run(show_resp(chat))

if __name__ == '__main__':
    main()
