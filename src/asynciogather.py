import asyncio
import time


async def fetch_data(name, delay):
    print(f"开始获取 {name} 数据...")
    await asyncio.sleep(delay)
    print(f"{name} 数据获取完成")
    return f"{name} 的数据"


async def main():
    print(f"开始时间: {time.strftime('%X')}")
    results = await asyncio.gather(
        fetch_data("用户信息", 1),
        fetch_data("订单信息", 2),
        fetch_data("商品信息", 1.5)
    )
    print("所有信息获取完成:")
    for result in results:
        print(result)
    print(f"结束时间 {time.strftime('%X')}")

if __name__ == "__main__":
    asyncio.run(main())
    """
    开始时间: 18:34:27
    开始获取 用户信息 数据...
    开始获取 订单信息 数据...
    开始获取 商品信息 数据...
    用户信息 数据获取完成
    商品信息 数据获取完成
    订单信息 数据获取完成
    所有信息获取完成:
    用户信息 的数据
    订单信息 的数据
    商品信息 的数据
    结束时间 18:34:29
    """