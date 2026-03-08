import asyncio
import aiohttp
import asyncpg
from bs4 import BeautifulSoup
from core import load_env
import os
from pathlib import Path

def parse_html(html):

    soup = BeautifulSoup(html, "html.parser")

    title = ''
    description = ''

    if soup.title:
        title = soup.title.string

    meta = soup.find("meta", attrs={"name": "description"})

    if meta:
        description = meta.get("content")

    return title, description


async def fetch(session, url, retries=3):

    for attempt in range(retries):

        try:
            async with session.get(url, timeout=10) as response:

                if response.status != 200:
                    raise Exception("Bad response")

                return await response.text()

        except Exception:

            if attempt == retries - 1:
                print("Failed:", url)

            await asyncio.sleep(1)


async def save_to_db(pool, url, title, description):

    async with pool.acquire() as conn:

        await conn.execute(
            """
            INSERT INTO pages(url,title,description)
            VALUES($1,$2,$3)
            """,
            url,
            title,
            description
        )

async def worker(session, url, semaphore, pool):

    async with semaphore:

        html = await fetch(session, url)

        if not html:
            return

        title, description = parse_html(html)

        await save_to_db(pool, url, title, description)

        print("Saved url:", url)


async def main():

    BASE_DIR = Path(__file__).resolve().parents[3]

    file = os.path.join(BASE_DIR, 'urls.txt')

    with open(file) as f:
        urls = [line.strip() for line in f]

    semaphore = asyncio.Semaphore(20)

    pool = await asyncpg.create_pool(
        user=load_env.POSTGRES_USER,
        password=load_env.POSTGRES_PASSWORD,
        database=load_env.POSTGRES_DB,
        host=load_env.POSTGRES_HOST,
        port=load_env.POSTGRES_PORT,
        min_size=5,
        max_size=20
    )

    async with aiohttp.ClientSession() as session:

        tasks = [
            worker(session, url, semaphore, pool)
            for url in urls
        ]

        await asyncio.gather(*tasks)

    await pool.close()


if __name__ == "__main__":
    asyncio.run(main())