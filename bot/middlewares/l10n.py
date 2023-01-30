from typing import Callable, Dict, Any, Awaitable, Optional

from aiogram import BaseMiddleware, types
from aiogram.types import Message, User
from fluentogram import TranslatorHub

from utils.databases.postgres import DataBase


class L10nMiddleware(BaseMiddleware):
    def __init__(self, t_hub: TranslatorHub):
        self.t_hub = t_hub

    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:
        user: Optional[User] = types.User.get_current()
        get_lang_code = await DataBase.execute(
            'SELECT lang_code FROM users WHERE telegram_id = $1',
            int(user.id), fetchval=True
        )

        if not get_lang_code:
            get_lang_code = 'en'

        data["l10n"] = self.t_hub.get_translator_by_locale(get_lang_code)
        data["t_hub"] = self.t_hub
        await handler(event, data)
