import asyncio


async def my_coroutine():
    print("start")
    await asyncio.sleep(1)
    print("continue")
    return "end"


if __name__ == "__main__":
    res=asyncio.run(my_coroutine())
    print(res)
