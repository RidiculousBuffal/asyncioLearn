import asyncio
import time


async def say_after(delay, what):
    await asyncio.sleep(delay)
    print(what)


async def main():
    print(f"开始时间 {time.strftime('%X')}")
    task1 = asyncio.create_task(say_after(1, 'hello'))
    task2 = asyncio.create_task(say_after(2, 'world'))
    await task1
    await task2
    print(f"结束时间: {time.strftime('%X')}")

if __name__ == '__main__':
    asyncio.run(main())
    """
    开始时间 13:43:50
    hello
    world
    结束时间: 13:43:52
    """
