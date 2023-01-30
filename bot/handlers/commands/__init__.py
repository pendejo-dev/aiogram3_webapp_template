from aiogram import Router
from aiogram.filters import Command
from magic_filter import F

from bot.handlers.commands.main import cmd_menu
from bot.handlers.commands.start import cmd_start


def register_user_commands(router: Router):
    router.message.register(cmd_start, Command(commands='start'), F.chat.type == 'private')
    router.message.register(cmd_menu, Command(commands='menu'), F.chat.type == 'private')
