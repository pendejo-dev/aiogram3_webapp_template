from typing import Optional

from aiogram import types, Bot
from aiogram.filters import CommandObject
from aiogram.fsm.context import FSMContext
from fluentogram import TranslatorRunner


async def cmd_start(message: types.Message, state: FSMContext, bot: Bot, l10n: TranslatorRunner,
                    command: Optional[CommandObject] = None):
    await state.set_state(None)
