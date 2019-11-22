# Import modules ----------------------------
import os
import json
import logging
from telethon import TelegramClient
from datetime import datetime
from tgscrape.requesters.query_channel import query_channel
from tgscrape.utils import parse_entities_configs

# Setup ------------------------------------

# setup logger
log_path=None
if log_path is None:
    log_path='logs'
    if not os.path.exists(log_path):
        os.mkdir(log_path)

# create logger
logger=logging.getLogger()
logger.setLevel(logging.INFO)

# create console handler and set level to debug
fh=logging.FileHandler(
    filename=os.path.join(log_path, 'tg_dump_%s.log' % datetime.today().strftime('%Y-%m-%d')),
    mode='a',
    encoding='utf-8'
)
fh.setLevel(logging.INFO)

# create formatter
formatter=logging.Formatter('%(asctime)s: %(name)s: %(levelname)s: %(message)s',  '%Y-%m-%d %H:%M:%S')

# add formatter to ch
fh.setFormatter(formatter)

# add ch to logger
logger.addHandler(fh)

# output directory
dump_path=os.path.join(os.getenv('HOME'), 'Dropbox', 'tgdump', 'channels')


# get API access keys
secrets_path = os.path.expanduser(os.getenv('SECRETS'))
tg_api_secrets = os.path.join(secrets_path, 'telegram_api_dlchats.json')

with open (tg_api_secrets) as f: tg_api_secrets = json.load(f)


# start telegram API client
client = TelegramClient(
    os.path.join(secrets_path, 'telethon.session'),
    api_id=tg_api_secrets['api_id'],
    api_hash=tg_api_secrets['api_hash']
)

async def start_client(client):
    await client.start()
    await client.connect()
    assert client.is_connected(), False

    return True


with client: is_connected = client.loop.run_until_complete(start_client(client))

if not is_connected:
    logger.error('Cannot connect to Telegram Client. Aborting')
    

# Get entities data from API --------------------------------------

# get entities
entities_dir=os.path.join('config', 'tgentities')
entities=parse_entities_configs(path=entities_dir)

channel_data={}

with client:
    for file, data in entities.items():
        logger.info('Requesting data for entities listed in file %s', file)
        for entry in data:
            if entry['kind'] == 'channel':
                chan=entry['username']
                try:
                    channel_data[chan] = client.loop.run_until_complete(query_channel(client, channel=chan, until=datetime.now().date()))
                except:
                    logger.warning('Could not get channel info, messages and participants data for channel "%s"', chan)
                    continue
                logger.info('Successfully got channel info, messages and participants data for channel "%s"', chan)
            else:
                logger.warning('Data request for entities of type "%s" not implemented. Ignoring username "%s"', entry['kind'], entry['username'])

# Write channel data to disk --------------------------------------
for chan, data in channel_data.items():
    fp=os.path.join(dump_path, chan + '.json')
    update=os.path.exists(fp)
    try:
        with open(fp, 'w', encoding='utf-8') as dest:
            data.to_json(dest, indent=4)
    except:
        logger.error('Could not %s channel info, messages and participants data for channel "%s".', 'update' if update else 'write', chan)
        continue

    logger.info('%s channel info, messages and participants data for channel "%s" to disk at %s', 'Updated' if update else 'Wrote', chan, fp)


# remove handlers
for hdl in logger.handlers:
    logger.removeHandler(hdl)

world='world'
print(f'hi {world}')
