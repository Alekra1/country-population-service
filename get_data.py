import asyncio

from config import Settings
from repository import CountryRepository
from sources.statisticstimes import StatisticsTimesSource
from sources.wikipedia import WikipediaSource


class GetDataApp:
    def get_source(self):
        settings = Settings()
        match settings.data_source:
            case "wikipedia":
                return WikipediaSource()
            case "statisticstimes":
                return StatisticsTimesSource()
            case _:
                raise ValueError("unknown value of the data_source variable")

    async def run(self):
        repo = CountryRepository()
        source = self.get_source()
        await repo.init_schema()
        countries = await source.fetch_data()
        await repo.replace_all(countries)


asyncio.run(GetDataApp().run())
