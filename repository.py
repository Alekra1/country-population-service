import asyncpg

from config import Settings
from models import Country


class CountryRepository:
    def __init__(self):
        self.settings = Settings()
        self.url = f"postgresql://{self.settings.user}:{self.settings.password}@{self.settings.host}:{self.settings.port}/{self.settings.name}"

    async def init_schema(self):
        conn = await asyncpg.connect(self.url)
        try:
            await conn.execute(
                "CREATE TABLE IF NOT EXISTS countries(id SERIAL PRIMARY KEY,name TEXT,region TEXT,population BIGINT);"
            )

        finally:
            await conn.close()

    async def replace_all(self, countries: list[Country]):
        conn = await asyncpg.connect(self.url)
        try:
            async with conn.transaction():
                await conn.execute("TRUNCATE TABLE countries RESTART IDENTITY;")
                await conn.executemany(
                    "INSERT INTO countries (name, region, population) VALUES ($1, $2, $3)",
                    [
                        (country.name, country.region, country.population)
                        for country in countries
                    ],
                )

        finally:
            await conn.close()
