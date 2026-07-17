import asyncio

from repository import CountryRepository


class PrintDataApp:
    async def run(self):
        repo = CountryRepository()
        regions_statistics = await repo.region_stats()
        for region in regions_statistics:
            print(f"Region: {region.region_name}")
            print(f"Total Population: {region.total_population}")
            print(f"Largest Country: {region.largest_country_name}")
            print(f"Largest Population: {region.largest_country_population}")
            print(f"Smallest Country: {region.smallest_country_name}")
            print(f"Smallest Population: {region.smallest_country_population}")


asyncio.run(PrintDataApp().run())
