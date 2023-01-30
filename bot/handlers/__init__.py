from aiogram import Dispatcher, Router

from bot.handlers.callbacks import register_callbacks_query
from bot.handlers.commands import register_user_commands


def setup_routers(dp: Dispatcher):
    default_router = Router()
    dp.include_router(default_router)

    register_user_commands(default_router)  # Команды пользователя.
    register_callbacks_query(default_router)  # Нажатые inline-кнопки.
