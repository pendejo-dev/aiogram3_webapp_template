from aiogram import Bot
from aiogram.types import BotCommandScopeDefault, BotCommand


async def set_bot_commands(bot: Bot):
    usercommands = [
        BotCommand(command="menu", description="Главное меню"),
    ]
    await bot.set_my_commands(usercommands, scope=BotCommandScopeDefault())

