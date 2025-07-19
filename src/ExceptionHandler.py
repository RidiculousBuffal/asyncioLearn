import asyncio
import random


async def risky_operation(name):
    await asyncio.sleep(1)
    if random.random() < 0.5:
        raise ValueError(f"操作 {name} 失败了!")
    return f"操作 {name} 成功"


async def safe_operation(name):
    try:
        result = await risky_operation(name)
        print(result)
        return result
    except ValueError as e:
        print(f"捕获异常: {e}")
        return f"操作 {name} 失败"


async def main():
    tasks = [
        asyncio.create_task(safe_operation("A")),
        asyncio.create_task(safe_operation("B")),
        asyncio.create_task(safe_operation("C"))
    ]

    results = await asyncio.gather(*tasks)
    print(f"最终结果: {results}")

if __name__ == '__main__':
    asyncio.run(main())