from telethon.tl.types import Channel
from telethon.tl.types import ChannelFull, PeerNotifySettings, ChatInviteEmpty, PhotoEmpty
from telethon.tl.types.messages import ChannelMessages, ChatFull
from telethon.tl.types.channels import ChannelParticipants
from datetime import datetime
import json
from telethon.tl.tlobject import _json_default

class ChannelData(Channel):
    def __init__(self, id: int, username: str, channel_info: [ChatFull, type(None)], channel_messages: [ChannelMessages, type(None)], channel_participants: [ChannelParticipants, type(None)]):
        """
        :type id: int
        :type username: str
        :type channel_info: telethon.tl.types.messages.ChatFull
        :type channel_messages: telethon.tl.types.messages.ChannelMessages
        :type channel_participants: telethon.tl.types.channels.ChannelParticipants
        :type created_at: datetime.datetime
        """
        self.id = id
        self.username = username

        if channel_info is None:
            self.channel_info=ChatFull(
                full_chat=ChannelFull(
                    id=0,
                    about='not valid',
                    pts=0,
                    read_inbox_max_id=0,
                    read_outbox_max_id=0,
                    unread_count=0,
                    chat_photo=PhotoEmpty(id=0),
                    bot_info=[],
                    notify_settings=PeerNotifySettings(),
                    exported_invite=ChatInviteEmpty()
                ),
                chats=[],
                users=[]
            )
        else:
            assert isinstance(channel_info, ChatFull), 'Value passed to constructor argument "channel_info" must be None or an object of type <telethon.tl.types.ChatFull>'
            assert channel_info.to_dict()['full_chat']['id']==id, 'Value passed to constructor argument "id" and value .to_dict()[\'full_chat\'][\'id\'] of object passed to argument "channel_info" do not match'
            assert len(channel_info.to_dict()['chats'])==1, 'List .to_dict()[\'full_chat\'][\'id\'] of object passed to argument "channel_info" contains more than one object'
            assert channel_info.to_dict()['chats'][0]['username'] == username, 'Value passed to constructor argument "username" and value .to_dict()[\'chats\'][0][\'username\'] of object passed to argument "channel_info" do not match'
            self.channel_info=channel_info

        if channel_messages is None:
            self.channel_messages=ChannelMessages(pts=0, count=0, messages=[], chats=[], users=[])
        else:
            assert isinstance(channel_messages, ChannelMessages), 'Value passed to constructor argument "channel_message" must be None or an object of type <telethon.tl.types.messages.ChannelMessages>'
            self.channel_messages=channel_messages

        if channel_participants is None:
            self.channel_participants=ChannelParticipants(count=0, participants=[], users=[])
        else:
            assert isinstance(channel_participants,
                              ChannelParticipants), 'Value passed to constructor argument "channel_participants" must be None or an object of type <telethon.tl.types.channels.ChannelParticipants>'
            self.channel_participants=channel_participants

        self.created_at=datetime.now()

    def to_dict(self):
        out = dict()
        out['_'] = 'ChannelData'
        for attr in self.__dict__.keys():
            try:
                out[str(attr)] = getattr(self, attr).to_dict()
            except:
                out[str(attr)] = getattr(self, attr)
        return out

    def to_json(self, fp=None, default=_json_default, **kwargs):
        """
        Represent the current `ChannelData` as JSON.
        If ``fp`` is given, the JSON will be dumped to said
        file pointer, otherwise a JSON string will be returned.
        Note that bytes and datetimes cannot be represented
        in JSON, so if those are found, they will be base64
        encoded and ISO-formatted, respectively, by default.
        """
        d = self.to_dict()
        if fp:
            return json.dump(d, fp, default=default, **kwargs)
        else:
            return json.dumps(d, default=default, **kwargs)




