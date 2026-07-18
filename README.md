# Country population service

Loads per-country population data into Postgres and prints per-region summaries. Runs via Docker Compose.

## Requirements

- Docker with Compose

## Run

```bash
git clone https://github.com/Alekra1/country-population-service.git
cd country-population-service
docker compose up get_data
docker compose up print_data
```

Postgres starts automatically (`db` service, healthchecked). Both app services share one image.

## What it does

- **`get_data`** — fetches a population table, validates rows, stores **unaggregated** country records (replace-all on each run).
- **`print_data`** — aggregates with **one SQL query** and prints, per region:
  - region name
  - total population
  - largest country + population
  - smallest country + population

Output lines are labeled for readability; field order matches the task.

**Region** means UN continental region (Wikipedia) or continent (StatisticsTimes). Dependencies are kept as separate rows, as in the source tables.

## Data source

Switch with `DATA_SOURCE` (used by `get_data`):

| Value              | Source |
|--------------------|--------|
| `wikipedia` (default) | [UN list on Wikipedia](https://en.wikipedia.org/w/index.php?title=List_of_countries_by_population_(United_Nations)&oldid=1215058959) |
| `statisticstimes`  | [StatisticsTimes](https://statisticstimes.com/demographics/countries-by-population.php) |

Examples:

```bash
DATA_SOURCE=wikipedia docker compose up get_data
DATA_SOURCE=statisticstimes docker compose up get_data
docker compose up print_data
```

Each `get_data` run replaces the table. `print_data` summarizes whatever was loaded last. Region names can differ between sources.

## Stack

Python 3.13, httpx, BeautifulSoup4, pydantic, asyncpg, Postgres 18 — async end to end. Class-based layout (`DataSource`, `CountryRepository`, `GetDataApp`, `PrintDataApp`).
