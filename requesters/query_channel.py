from datetime import datetime, timedelta, timezone
from telethon import functions, types
from telethon.client.telegramclient import TelegramClient
from tgscrape.custom.channel import ChannelData

async def query_channel(client: TelegramClient, channel: str, until=None, lim=1000000000) -> dict:

    """Request telegram channel info, chat history and participants
    :param client: object of class telethon.client.telegramclient.TelegramClient
    :param channel: (str)
    :param until: object of class datetime.datetime
    :param lim: integer
    :param tsfmt: string specifying the time stamp format
    :return: an instance of tgscrape.custom.ChannelData
    :rtype: tgscrape.custom.ChannelData
    """

    if until is None:
        until = datetime.today().date() + timedelta(days=1)
        until = datetime.combine(until, datetime.min.time(), timezone.utc)

    out = dict()

    out['info'] = await client(functions.channels.GetFullChannelRequest(channel))


    chats=out['info'].to_dict()['chats']
    assert len(chats)==1
    print(chats[0]['username'])
    assert chats[0]['username']==channel

    id = out['info'].to_dict()['full_chat']['id']

    out['messages'] = await client(functions.messages.GetHistoryRequest(
        peer=channel,
        offset_id=0,
        offset_date=until,
        add_offset=0,
        limit=lim,
        min_id=0,
        max_id=0,
        hash=0
    ))

    out['participants'] = await client(functions.channels.GetParticipantsRequest(
        channel=channel,
        filter=types.ChannelParticipantsRecent(),
        offset=0,
        limit=lim,
        hash=0
    ))

    return ChannelData(id=id, username=channel, channel_info=out['info'], channel_messages=out['messages'], channel_participants=out['participants'])

