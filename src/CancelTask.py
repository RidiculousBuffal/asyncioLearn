import asyncio
import time


async def long_running_task(name, duration):
    """长时间运行的任务"""
    try:
        print(f"任务 {name} 开始执行")
        for i in range(duration):
            await asyncio.sleep(1)
            print(f"任务 {name} 执行中... {i + 1}/{duration}  当前时间 {time.strftime('%X')}")
            """
            在这一秒钟，任务 A、B、C 都完成了它们的 sleep(1)，都处于“准备就绪”状态。事件循环现在需要决定先恢复哪一个。
            虽然在大多数情况下，它可能会遵循一个可预测的模式（比如任务创建的顺序），但 asyncio 的官方文档并没有保证恢复的顺序。
            因此，你不能依赖于“任务A执行中...1/5”一定会在“任务B执行中...1/3”之前打印。这个恢复顺序取决于事件循环的具体实现和当时的状态。
            """
        print(f"任务 {name} 完成")
        return f"任务 {name} 的结果"
    except asyncio.CancelledError:
        print(f"任务 {name} 被取消")
        raise


async def task_cancellation_example():
    """任务取消示例"""
    # 创建任务
    print(f" 当前时间 {time.strftime('%X')}")
    task1 = asyncio.create_task(long_running_task("A", 5))
    task2 = asyncio.create_task(long_running_task("B", 3))
    task3 = asyncio.create_task(long_running_task("C", 4))

    # 等待2秒后取消任务A
    await asyncio.sleep(2)
    task1.cancel()
    print(f"取消了任务1 当前时间 {time.strftime('%X')}")

    # 等待剩余任务完成
    results = await asyncio.gather(task1, task2, task3, return_exceptions=True)

    print("任务结果:")
    for i, result in enumerate(results, 1):
        if isinstance(result, asyncio.CancelledError):
            print(f"  任务{chr(64 + i)}: 已取消")
        elif isinstance(result, Exception):
            print(f"  任务{chr(64 + i)}: 异常 - {result}")
        else:
            print(f"  任务{chr(64 + i)}: {result}")


if __name__ == "__main__":
    asyncio.run(task_cancellation_example())
    """
     当前时间 21:12:23
任务 A 开始执行
任务 B 开始执行
任务 C 开始执行
任务 A 执行中... 1/5  当前时间 21:12:24
任务 B 执行中... 1/3  当前时间 21:12:24
任务 C 执行中... 1/4  当前时间 21:12:24
取消了任务1 当前时间 21:12:25
任务 B 执行中... 2/3  当前时间 21:12:25
任务 A 被取消
任务 C 执行中... 2/4  当前时间 21:12:25
任务 B 执行中... 3/3  当前时间 21:12:26
任务 B 完成
任务 C 执行中... 3/4  当前时间 21:12:26
任务 C 执行中... 4/4  当前时间 21:12:27
任务 C 完成
任务结果:
  任务A: 已取消
  任务B: 任务 B 的结果
  任务C: 任务 C 的结果
    """