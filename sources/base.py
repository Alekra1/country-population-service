from abc import ABC, abstractmethod

from models import Country


class DataSource(ABC):
    @abstractmethod
    async def fetch_data(self) -> list[Country]: ...
