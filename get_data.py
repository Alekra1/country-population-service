import asyncio

from repository import CountryRepository
from sources.wikipedia import WikipediaSource


class GetDataApp:
    async def run(self):
        repo = CountryRepository()
        wiki = WikipediaSource()
        await repo.init_schema()
        countries = await wiki.fetch_data()
        await repo.replace_all(countries)


asyncio.run(GetDataApp().run())
