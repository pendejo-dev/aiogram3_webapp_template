from aiogram import types, Bot
from aiogram.fsm.context import FSMContext
from fluentogram import TranslatorRunner


async def cmd_menu(message: types.Message, state: FSMContext, bot: Bot, l10n: TranslatorRunner):
    await state.set_state(None)
