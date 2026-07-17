from pydantic import BaseModel, Field, field_validator


class Country(BaseModel):
    name: str
    region: str
    population: int = Field(gt=0)

    @field_validator("name")
    @classmethod
    def clean_name(cls, value: str) -> str:
        idx_to_strip = value.find("[")
        if idx_to_strip == -1:
            return value.strip()
        return value[:idx_to_strip].strip()

    @field_validator("population", mode="before")
    @classmethod
    def normalize_population(cls, value: str) -> str:
        return value.replace(",", "")


class RegionStats(BaseModel):
    region_name: str
    total_population: int
    largest_country_name: str
    largest_country_population: int
    smallest_country_name: str
    smallest_country_population: int
