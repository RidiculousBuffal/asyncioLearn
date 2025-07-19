import asyncio
import time


async def say_after(delay, what):
    await asyncio.sleep(delay)
    print(what)


async def main():
    print(f"开始时间:{time.strftime('%X')}")
    await say_after(1, 'hello')
    await say_after(2, 'world')
    print(f"结束时间:{time.strftime('%X')}")

if __name__ == '__main__':
    asyncio.run(main())
    """
    开始时间:13:30:24
    hello
    world
    结束时间:13:30:27
    """
