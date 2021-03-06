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

import pyrogram
from pyrogram.api import functions
from pyrogram.client.ext import BaseClient, utils


class EditInlineText(BaseClient):
    def edit_inline_text(
        self,
        inline_message_id: str,
        text: str,
        parse_mode: str = "",
        disable_web_page_preview: bool = None,
        reply_markup: "pyrogram.InlineKeyboardMarkup" = None
    ) -> bool:
        """Edit the text of **inline** messages.

        Parameters:
            inline_message_id (``str``):
                Identifier of the inline message.

            text (``str``):
                New text of the message.

            parse_mode (``str``, *optional*):
                Pass "markdown" or "html" if you want Telegram apps to show bold, italic, fixed-width text or inline
                URLs in your message. Defaults to "markdown".

            disable_web_page_preview (``bool``, *optional*):
                Disables link previews for links in this message.

            reply_markup (:obj:`InlineKeyboardMarkup`, *optional*):
                An InlineKeyboardMarkup object.

        Returns:
            ``bool``: On success, True is returned.

        Raises:
            RPCError: In case of a Telegram RPC error.
        """
        style = self.html if parse_mode.lower() == "html" else self.markdown

        return self.send(
            functions.messages.EditInlineBotMessage(
                id=utils.unpack_inline_message_id(inline_message_id),
                no_webpage=disable_web_page_preview or None,
                reply_markup=reply_markup.write() if reply_markup else None,
                **style.parse(text)
            )
        )
