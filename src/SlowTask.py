import asyncio


async def slow_operation(name, delay):
    """慢速操作"""
    print(f"开始执行 {name}...")
    await asyncio.sleep(delay)
    print(f"{name} 完成")
    return f"{name} 的结果"


async def timeout_example():
    """超时控制示例"""
    tasks = [
        ("快速任务", 1),
        ("中速任务", 3),
        ("慢速任务", 5)
    ]

    for name, delay in tasks:
        try:
            # 设置3秒超时
            result = await asyncio.wait_for(
                slow_operation(name, delay),
                timeout=3.0
            )
            print(f"✅ {result}")
        except asyncio.TimeoutError:
            print(f"❌ {name} 超时")
        print()

# 运行示例
if __name__ == '__main__':
    asyncio.run(timeout_example())