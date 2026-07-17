import httpx
from bs4 import BeautifulSoup
from pydantic import ValidationError

from models import Country
from sources.base import DataSource

URL = "https://en.wikipedia.org/w/index.php?title=List_of_countries_by_population_(United_Nations)&oldid=1215058959"


class WikipediaSource(DataSource):
    async def fetch_data(self) -> list[Country]:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(
                URL, headers={"User-Agent": "population-parser"}
            )
            response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        table = soup.select_one(".wikitable")
        if table is None:
            raise RuntimeError("Table not found")

        rows = table.find_all("tr")

        failed_countries = []
        countries: list[Country] = []
        for row in rows:
            data = row.find_all("td")
            if len(data) < 5:
                continue
            name = data[0].get_text()
            if "World" in name:
                continue
            population = data[2].get_text()
            region = data[4].get_text()
            try:
                country = Country(name=name, region=region, population=population)
                countries.append(country)
            except ValidationError:
                failed_countries.append(name.strip())
        return countries
