import asyncio
import os

import aiohttp
import time
import dotenv
dotenv.load_dotenv()

async def fetch_url(session, url):
    try:
        async with session.get(url) as response:
            content = await response.json()
            return {
                'url': url,
                'status': response.status,
                'content': content
            }
    except Exception as e:
        return {
            'url': url,
            'error': str(e)
        }


async def fetch_multiple_urls():
    """并发获取多个URL"""
    urls = [
        'https://httpbin.org/delay/1',
        'https://httpbin.org/delay/2',
        'https://httpbin.org/delay/1',
        'https://httpbin.org/status/200',
        'https://httpbin.org/json'
    ]

    start_time = time.time()

    async with aiohttp.ClientSession() as session:
        tasks = [fetch_url(session, url) for url in urls]
        results = await asyncio.gather(*tasks)

    end_time = time.time()

    print(f"总耗时: {end_time - start_time:.2f}秒")
    for result in results:
        if 'error' in result:
            print(f"❌ {result['url']}: {result['error']}")
        else:
            print(f"✅ {result['url']}: {result['status']}\n"
                  f" {result['content']} ")


if __name__=='__main__':
    asyncio.run(fetch_multiple_urls())