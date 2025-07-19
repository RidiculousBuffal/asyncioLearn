import asyncio
import random
from asyncio import Semaphore


async def limited_resource_task(semaphore: Semaphore, task_id):
    """需要限制并发数的任务"""
    async with semaphore:
        print(f"任务 {task_id} 开始执行")
        # 模拟工作
        await asyncio.sleep(random.uniform(1, 3))
        print(f"任务 {task_id} 完成")
        return f"任务 {task_id} 的结果"


async def semaphore_example():
    """信号量控制并发示例"""
    # 创建信号量，最多允许3个并发任务
    semaphore = asyncio.Semaphore(3)

    # 创建10个任务
    tasks = [
        limited_resource_task(semaphore, i)
        for i in range(1, 11)
    ]

    print("开始执行任务（最多3个并发）...")
    results = await asyncio.gather(*tasks)

    print("所有任务完成:")
    for result in results:
        print(f"  {result}")


if __name__ == "__main__":
    asyncio.run(semaphore_example())
