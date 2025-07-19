import asyncio
import random


async def producer(queue: asyncio.Queue, producer_id):
    """生产者：生产10个项目，然后结束"""
    for i in range(10):
        item = f"Producer-{producer_id}-Item-{i}"
        await queue.put(item)
        print(f"生产者{producer_id} 生产了 {item}")
        await asyncio.sleep(random.uniform(0.5, 1.5))
    print(f"生产者 {producer_id} 完成")


async def consumer(queue: asyncio.Queue, consumer_id):
    """消费者：持续消费，直到收到None信号"""
    while True:
        item = await queue.get()
        if item is None:
            break
        print(f"消费者{consumer_id} 消费了: {item}")
        await asyncio.sleep(random.uniform(0.5, 2.5))
    print(f"消费者 {consumer_id} 结束")


async def queue_example():
    queue = asyncio.Queue(maxsize=5)

    # 创建生产者和消费者任务
    producers = [
        asyncio.create_task(producer(queue, i))
        for i in range(1, 3)
    ]
    consumers = [
        asyncio.create_task(consumer(queue, i))
        for i in range(1, 4)
    ]

    # 1. 等待所有生产者完成
    await asyncio.gather(*producers)
    print("所有生产者都已完成生产。")
    # 2. 为每个消费者发送一个终止信号
    for _ in consumers:
        await asyncio.sleep(random.uniform(0.5, 1.5))
        await queue.put(None)
    print("已发送所有终止信号。")

    # 3. 等待所有消费者完成它們的任务
    await asyncio.gather(*consumers)
    print("所有消费者都已正常关闭。")


if __name__ == '__main__':
    asyncio.run(queue_example())
