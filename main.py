import asyncio
import json
import logging

import uvicorn
from fastapi import FastAPI, Response
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from models import SearchQuery
from scrapers.norgau import bulk_scrape
from scrapers import norgau


all_scrapers = [
    norgau
]


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/ping")
async def ping():
    return "pong"


@app.get("/page", response_class=HTMLResponse)
async def read_root():
    with open(file="index.html", mode="r", encoding="utf-8") as f:
        html = f.read()
    return HTMLResponse(content=html, status_code=200)


@app.get("/test", response_class=HTMLResponse)
async def read_root():
    with open(file="test.html", mode="r", encoding="utf-8") as f:
        html = f.read()
    return HTMLResponse(content=html, status_code=200)


@app.post("/scrape")
async def scrape(sq: SearchQuery):
    return sq.search_query  # "pong"


@app.get("/scrape")
async def scrape():
    async with asyncio.TaskGroup() as tg:
        tasks = []
        for scraper in all_scrapers:
            task = tg.create_task(scraper.bulk_scrape("штангенциркуль"))
            tasks.append(task)
    response = await asyncio.gather(*tasks)
    print(response)
    return Response(
        content=json.dumps(response, indent=4, ensure_ascii=False),
        headers={'Content-type': 'application/json'}
    )  # sq.search_query


@app.get("/time", response_class=HTMLResponse)
async def read_root():
    with open(file="index.html", mode="r", encoding="utf-8") as f:
        html = f.read()
    return HTMLResponse(content=html, status_code=200)


def start():
    if __name__ == "__main__":
        uvicorn.run(app="main:app",
                    host="0.0.0.0",
                    port=5005,
                    log_level="info",
                    )


start()
