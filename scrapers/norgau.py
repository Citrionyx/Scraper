import asyncio
import json
import time
import aiohttp
from aiohttp_socks import ProxyConnector
from parsel import Selector


def get_name() -> str:
    return "NORGAU"


def get_url() -> str:
    return "https://norgau.com"


async def bulk_scrape(query) -> list | dict:
    func_start = time.time()
    url = f"https://norgau.com/search/?PAGEN_1=1&sort=popular-descending&size=500&q={query}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(url=url, headers=headers) as resp:
            # print(resp.status)
            # print(await resp.text())
            response = await resp.text()

    html = Selector(text=response)

    scripts = html.css("script").getall()

    data_begin_rp = "window.globalData[\"catalog\"][\'products\'] = "

    data_script = None

    for script in scripts:
        if data_begin_rp in script:
            data_script = script

    if not data_script:
        return {"error": "Failed to find a script containing data, or there is no such product."}

    begin = data_script.find(data_begin_rp) + len(data_begin_rp)
    end = data_script[begin:].find("}];") + begin + 2

    data = json.loads(data_script[begin:end])

    parts_data_list = []

    for product in data:
        parts_data_list.append({
            "product_store": get_name(),
            "product_name": product["desc"],
            "product_article": product["id"],
            "product_in_stock": product["available"],
            "product_price": product["prices"]["base"],
            "product_link": "".join((get_url(), product["href"])),
            "product_image": "".join((get_url(), product["images"][0])),
        })
    print(f"{query} time:", time.time() - func_start)
    return parts_data_list


# start = time.time()


# print(json.dumps(bulk_scrape("ошщарпомвам"), ensure_ascii=False, indent=4))


# async def pr(te, n=0):
#     await asyncio.sleep(n)
#     print(te)
#
#
# async def test():
#     async with asyncio.TaskGroup() as tg:
#         words = ["гайковерт", "весы", "требушет", "штангенциркуль"]
#         tasks = []
#         for word in words:
#             task = tg.create_task(bulk_scrape(word))
#             tasks.append(task)
#
#         return asyncio.gather(*tasks)
#
#
# print(asyncio.run(test()))

# print(time.time() - start)
