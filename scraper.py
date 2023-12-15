import asyncio
from scrapers import norgau


all_scrapers = [
    norgau
]


async def scrape(query):
    async with asyncio.TaskGroup() as tg:
        tasks = []
        for scraper in all_scrapers:
            task = tg.create_task(scraper.bulk_scrape(query))
            tasks.append(task)

        return asyncio.gather(*tasks)


print(asyncio.run(scrape("штангенциркуль")).result)
