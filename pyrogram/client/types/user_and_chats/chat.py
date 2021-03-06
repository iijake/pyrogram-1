# Pyrogram - Telegram MTProto API Client Library for Python
# Copyright (C) 2017-2019 Dan Tès <https://github.com/delivrance>
#
# This file is part of Pyrogram.
#
# Pyrogram is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Pyrogram is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Pyrogram.  If not, see <http://www.gnu.org/licenses/>.

from typing import Union

import pyrogram
from pyrogram.api import types
from .chat_permissions import ChatPermissions
from .chat_photo import ChatPhoto
from ..object import Object


class Chat(Object):
    """A chat.

    Parameters:
        id (``int``):
            Unique identifier for this chat.

        type (``str``):
            Type of chat, can be either "private", "bot", "group", "supergroup" or "channel".

        is_verified (``bool``, *optional*):
            True, if this chat has been verified by Telegram. Supergroups, channels and bots only.

        is_restricted (``bool``, *optional*):
            True, if this chat has been restricted. Supergroups, channels and bots only.
            See *restriction_reason* for details.

        is_scam (``bool``, *optional*):
            True, if this chat has been flagged for scam. Supergroups, channels and bots only.

        is_support (``bool``):
            True, if this chat is part of the Telegram support team. Users and bots only.

        title (``str``, *optional*):
            Title, for supergroups, channels and basic group chats.

        username (``str``, *optional*):
            Username, for private chats, bots, supergroups and channels if available.

        first_name (``str``, *optional*):
            First name of the other party in a private chat, for private chats and bots.

        last_name (``str``, *optional*):
            Last name of the other party in a private chat, for private chats.

        photo (:obj:`ChatPhoto`, *optional*):
            Chat photo. Suitable for downloads only.

        description (``str``, *optional*):
            Bio, for private chats and bots or description for groups, supergroups and channels.
            Returned only in :meth:`~Client.get_chat`.

        invite_link (``str``, *optional*):
            Chat invite link, for groups, supergroups and channels.
            Returned only in :meth:`~Client.get_chat`.

        pinned_message (:obj:`Message`, *optional*):
            Pinned message, for groups, supergroups channels and own chat.
            Returned only in :meth:`~Client.get_chat`.

        sticker_set_name (``str``, *optional*):
            For supergroups, name of group sticker set.
            Returned only in :meth:`~Client.get_chat`.

        can_set_sticker_set (``bool``, *optional*):
            True, if the group sticker set can be changed by you.
            Returned only in :meth:`~Client.get_chat`.

        members_count (``int``, *optional*):
            Chat members count, for groups, supergroups and channels only.

        restriction_reason (``str``, *optional*):
            The reason why this chat might be unavailable to some users.
            This field is available only in case *is_restricted* is True.

        permissions (:obj:`ChatPermissions` *optional*):
            Information about the chat default permissions, for groups and supergroups.
    """

    __slots__ = [
        "id", "type", "is_verified", "is_restricted", "is_scam", "is_support", "title", "username", "first_name",
        "last_name", "photo", "description", "invite_link", "pinned_message", "sticker_set_name", "can_set_sticker_set",
        "members_count", "restriction_reason", "permissions"
    ]

    def __init__(
        self,
        *,
        client: "pyrogram.BaseClient" = None,
        id: int,
        type: str,
        is_verified: bool = None,
        is_restricted: bool = None,
        is_scam: bool = None,
        is_support: bool = None,
        title: str = None,
        username: str = None,
        first_name: str = None,
        last_name: str = None,
        photo: ChatPhoto = None,
        description: str = None,
        invite_link: str = None,
        pinned_message=None,
        sticker_set_name: str = None,
        can_set_sticker_set: bool = None,
        members_count: int = None,
        restriction_reason: str = None,
        permissions: "pyrogram.ChatPermissions" = None
    ):
        super().__init__(client)

        self.id = id
        self.type = type
        self.is_verified = is_verified
        self.is_restricted = is_restricted
        self.is_scam = is_scam
        self.is_support = is_support
        self.title = title
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.photo = photo
        self.description = description
        self.invite_link = invite_link
        self.pinned_message = pinned_message
        self.sticker_set_name = sticker_set_name
        self.can_set_sticker_set = can_set_sticker_set
        self.members_count = members_count
        self.restriction_reason = restriction_reason
        self.permissions = permissions

    @staticmethod
    def _parse_user_chat(client, user: types.User) -> "Chat":
        peer_id = user.id

        return Chat(
            id=peer_id,
            type="bot" if user.bot else "private",
            is_verified=getattr(user, "verified", None),
            is_restricted=getattr(user, "restricted", None),
            is_scam=getattr(user, "scam", None),
            is_support=getattr(user, "support", None),
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name,
            photo=ChatPhoto._parse(client, user.photo, peer_id),
            restriction_reason=user.restriction_reason,
            client=client
        )

    @staticmethod
    def _parse_chat_chat(client, chat: types.Chat) -> "Chat":
        peer_id = -chat.id

        return Chat(
            id=peer_id,
            type="group",
            title=chat.title,
            photo=ChatPhoto._parse(client, getattr(chat, "photo", None), peer_id),
            permissions=ChatPermissions._parse(getattr(chat, "default_banned_rights", None)),
            client=client
        )

    @staticmethod
    def _parse_channel_chat(client, channel: types.Channel) -> "Chat":
        peer_id = int("-100" + str(channel.id))

        return Chat(
            id=peer_id,
            type="supergroup" if channel.megagroup else "channel",
            is_verified=getattr(channel, "verified", None),
            is_restricted=getattr(channel, "restricted", None),
            is_scam=getattr(channel, "scam", None),
            title=channel.title,
            username=getattr(channel, "username", None),
            photo=ChatPhoto._parse(client, getattr(channel, "photo", None), peer_id),
            restriction_reason=getattr(channel, "restriction_reason", None),
            permissions=ChatPermissions._parse(getattr(channel, "default_banned_rights", None)),
            client=client
        )

    @staticmethod
    def _parse(client, message: types.Message or types.MessageService, users: dict, chats: dict) -> "Chat":
        if isinstance(message.to_id, types.PeerUser):
            return Chat._parse_user_chat(client, users[message.to_id.user_id if message.out else message.from_id])

        if isinstance(message.to_id, types.PeerChat):
            return Chat._parse_chat_chat(client, chats[message.to_id.chat_id])

        return Chat._parse_channel_chat(client, chats[message.to_id.channel_id])

    @staticmethod
    def _parse_dialog(client, peer, users: dict, chats: dict):
        if isinstance(peer, types.PeerUser):
            return Chat._parse_user_chat(client, users[peer.user_id])
        elif isinstance(peer, types.PeerChat):
            return Chat._parse_chat_chat(client, chats[peer.chat_id])
        else:
            return Chat._parse_channel_chat(client, chats[peer.channel_id])

    @staticmethod
    def _parse_full(client, chat_full: types.messages.ChatFull or types.UserFull) -> "Chat":
        if isinstance(chat_full, types.UserFull):
            parsed_chat = Chat._parse_user_chat(client, chat_full.user)
            parsed_chat.description = chat_full.about

            if chat_full.pinned_msg_id:
                parsed_chat.pinned_message = client.get_messages(
                    parsed_chat.id,
                    message_ids=chat_full.pinned_msg_id
                )
        else:
            full_chat = chat_full.full_chat
            chat = None

            for i in chat_full.chats:
                if full_chat.id == i.id:
                    chat = i

            if isinstance(full_chat, types.ChatFull):
                parsed_chat = Chat._parse_chat_chat(client, chat)

                if isinstance(full_chat.participants, types.ChatParticipants):
                    parsed_chat.members_count = len(full_chat.participants.participants)
            else:
                parsed_chat = Chat._parse_channel_chat(client, chat)
                parsed_chat.members_count = full_chat.participants_count
                parsed_chat.description = full_chat.about or None
                # TODO: Add StickerSet type
                parsed_chat.can_set_sticker_set = full_chat.can_set_stickers
                parsed_chat.sticker_set_name = getattr(full_chat.stickerset, "short_name", None)

            if full_chat.pinned_msg_id:
                parsed_chat.pinned_message = client.get_messages(
                    parsed_chat.id,
                    message_ids=full_chat.pinned_msg_id
                )

            if isinstance(full_chat.exported_invite, types.ChatInviteExported):
                parsed_chat.invite_link = full_chat.exported_invite.link

        return parsed_chat

    @staticmethod
    def _parse_chat(client, chat: Union[types.Chat, types.User, types.Channel]) -> "Chat":
        if isinstance(chat, types.Chat):
            return Chat._parse_chat_chat(client, chat)
        elif isinstance(chat, types.User):
            return Chat._parse_user_chat(client, chat)
        else:
            return Chat._parse_channel_chat(client, chat)

    def archive(self):
        """Bound method *archive* of :obj:`Chat`.

        Use as a shortcut for:

        .. code-block:: python

            client.archive_chats(-100123456789)

        Example:
            .. code-block:: python

                chat.archive()

        Returns:
            True on success.

        Raises:
            RPCError: In case of a Telegram RPC error.
        """

        return self._client.archive_chats(self.id)

    def unarchive(self):
        """Bound method *unarchive* of :obj:`Chat`.

        Use as a shortcut for:

        .. code-block:: python

            client.unarchive_chats(-100123456789)

        Example:
            .. code-block:: python

                chat.unarchive()

        Returns:
            True on success.

        Raises:
            RPCError: In case of a Telegram RPC error.
        """

        return self._client.unarchive_chats(self.id)
