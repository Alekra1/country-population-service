import asyncpg

from config import Settings
from models import Country, RegionStats


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

    async def region_stats(self) -> list[RegionStats]:
        conn = await asyncpg.connect(self.url)
        try:
            rows = await conn.fetch("""
            SELECT
                region,
                SUM(population) AS total_population,
                (array_agg(name ORDER BY population DESC))[1] AS largest_country,
                MAX(population) AS largest_population,
                (array_agg(name ORDER BY population ASC))[1] AS smallest_country,
                MIN(population) AS smallest_population
            FROM countries
            GROUP BY region
            ORDER BY region;
            """)
            regions_statistics = []
            for row in rows:
                region = RegionStats(
                    region_name=row["region"],
                    total_population=row["total_population"],
                    largest_country_name=row["largest_country"],
                    largest_country_population=row["largest_population"],
                    smallest_country_name=row["smallest_country"],
                    smallest_country_population=row["smallest_population"],
                )
                regions_statistics.append(region)
            return regions_statistics

        finally:
            await conn.close()
