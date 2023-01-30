import asyncio
import logging
from pathlib import Path

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.fsm.strategy import FSMStrategy
from aiogram.webhook.aiohttp_server import SimpleRequestHandler
from aiohttp import web
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from dotenv import load_dotenv

from fluent_compiler.bundle import FluentBundle
from fluentogram import TranslatorHub, FluentTranslator

from bot.middlewares import L10nMiddleware
from commands import set_bot_commands
from config_reader import config
from utils.databases.postgres import DataBase

# Создаем экземпляр таймера по Московскому времени.
scheduler = AsyncIOScheduler(timezone="Europe/Moscow")

# Загружаем наш конфиг
load_dotenv()

# Загружаем логгер.
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(name)s %(levelname)s:%(message)s')
logger = logging.getLogger(__name__)


async def main():
    logging.basicConfig(
        level=logging.ERROR,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )

    # Получение пути до каталога locales относительно текущего файла
    locales_dir = Path(__file__).parent.joinpath("locales")

    # Подгружаем наши переводы из файлов.
    t_hub = TranslatorHub(
        {"ua": ("ua", "ru", "en"),
         "ru": ("ru", "en"),
         "en": ("en",)},
        translators=[
            FluentTranslator(locale="en",
                             translator=FluentBundle.from_files("en-US", filenames=[f'{str(locales_dir)}/en'
                                                                                    f'/strings.ftl'],
                                                                use_isolating=False)),
            FluentTranslator(locale="ru",
                             translator=FluentBundle.from_files("ru-RU", filenames=[f'{str(locales_dir)}/ru'
                                                                                    f'/strings.ftl'],
                                                                use_isolating=False))],
        root_locale="en",
    )

    # Создаем экземпляр бота.
    bot = Bot(token=config.bot_token, parse_mode="HTML")

    # Выбираем тип хранилища.
    if config.fsm_mode == "redis":
        storage = RedisStorage.from_url(
            url=f"redis://default:{config.redis.password}@{config.redis.host}:{config.redis.port}",
            connection_kwargs={"decode_responses": True, "db": config.redis.db}
        )
    else:
        storage = MemoryStorage()

    dp = Dispatcher(storage=storage, fsm_strategy=FSMStrategy.USER_IN_CHAT)
    dp.message.middleware(L10nMiddleware(t_hub))
    dp.callback_query.middleware(L10nMiddleware(t_hub))

    # Регистрация /-команд в интерфейсе.
    await set_bot_commands(bot)

    # Запуск пула PostgreSQL.
    await DataBase.create_pool()

    logging.getLogger('apscheduler.executors.default').setLevel(logging.WARNING)
    logging.getLogger('aiogram.event').setLevel(logging.WARNING)

    try:
        if not config.webhook_domain:
            await bot.delete_webhook()
            await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
        else:
            # Выключаем логи от aiohttp
            aiohttp_logger = logging.getLogger("aiohttp.access")
            aiohttp_logger.setLevel(logging.CRITICAL)

            # Установка веб хука
            await bot.set_webhook(
                url=config.webhook_domain + config.webhook_path,
                drop_pending_updates=True,
                allowed_updates=dp.resolve_used_update_types()
            )
            logging.info("Бот запущен")

            # Создание сервера aiohttp
            app = web.Application(
                client_max_size=1024 ** 4,
                # middlewares=[middleware_jwt]
            )

            # Передаем экземпляр бота и переводчика.
            app["bot"] = bot
            app["translate"] = t_hub

            # setup_routes(app)

            SimpleRequestHandler(dispatcher=dp, bot=bot).register(app, path=config.webhook_path)
            runner = web.AppRunner(app)
            await runner.setup()
            site = web.TCPSite(runner, host=config.app_host, port=config.app_port)
            await site.start()

            # Бесконечный цикл
            await asyncio.Event().wait()
    finally:
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(main())
