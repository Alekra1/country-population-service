import logging

import httpx
from bs4 import BeautifulSoup
from pydantic import ValidationError

from models import Country
from sources.base import DataSource

logger = logging.getLogger(__name__)

URL = "https://statisticstimes.com/demographics/countries-by-population.php"


class StatisticsTimesSource(DataSource):
    async def fetch_data(self) -> list[Country]:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(
                URL, headers={"User-Agent": "population-parser"}
            )
            response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        table = soup.select_one("#table_id")
        if table is None:
            raise RuntimeError("Table not found")

        rows = table.find_all("tr")

        countries: list[Country] = []
        for row in rows:
            data = row.find_all("td")
            if len(data) < 9:
                continue
            name = data[0].get_text()
            if "World" in name:
                continue
            population = data[3].get_text()
            region = data[8].get_text()
            try:
                country = Country(name=name, region=region, population=population)
                countries.append(country)
            except ValidationError as exc:
                logger.warning("Skipping row %r: %s", name.strip(), exc)
        if not countries:
            raise RuntimeError("No countries parsed; page layout may have changed")
        return countries
