import os
from chattool import Chat

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