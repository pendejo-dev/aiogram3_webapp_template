from typing import Union

import asyncpg
from asyncpg import Connection, DuplicateTableError
from asyncpg.pool import Pool

from config_reader import config


class DataBaseClass:
    def __init__(self):
        self.pool: Union[Pool, None] = None

    async def create_pool(self):
        self.pool = self.pool = await asyncpg.create_pool(
            user=config.postgres_user,
            password=config.postgres_password,
            host=config.postgres_host,
            database=config.postgres_database
        )

    async def execute(self, command: str, *args,
                      fetch: bool = False,
                      fetchval: bool = False,
                      fetchrow: bool = False,
                      execute: bool = False):
        async with self.pool.acquire() as connection:
            connection: Connection
            async with connection.transaction():
                if fetch:
                    result = await connection.fetch(command, *args)
                elif fetchval:
                    result = await connection.fetchval(command, *args)
                elif fetchrow:
                    result = await connection.fetchrow(command, *args)
                elif execute:
                    result = await connection.execute(command, *args)
        return result


DataBase = DataBaseClass()