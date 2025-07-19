# Python asyncio并发编程详细教程

## 目录

1. [异步编程基础概念](#1-异步编程基础概念)
2. [asyncio简介](#2-asyncio简介)
3. [基础语法和概念](#3-基础语法和概念)
4. [基础代码示例](#4-基础代码示例)
5. [进阶应用](#5-进阶应用)
6. [高级特性](#6-高级特性)
7. [性能优化](#7-性能优化)
8. [最佳实践](#8-最佳实践)
9. [常见问题和解决方案](#9-常见问题和解决方案)
10. [实际项目应用](#10-实际项目应用)

---

## 1. 异步编程基础概念

### 1.1 什么是异步编程

异步编程是一种编程范式，它允许程序在等待某些操作完成（如I/O操作）时继续执行其他任务，而不是阻塞等待。这种编程方式特别适合处理I/O密集型任务，如网络请求、文件读写、数据库操作等。

### 1.2 同步 vs 异步

**同步编程（Synchronous Programming）：**
- 代码按顺序执行，一行执行完毕后再执行下一行
- 遇到耗时操作时，程序会阻塞等待
- 简单直观，但效率较低

**异步编程（Asynchronous Programming）：**
- 允许程序在等待某个操作完成时执行其他任务
- 不会阻塞程序的执行
- 复杂度较高，但效率更高

### 1.3 并发 vs 并行

**并发（Concurrency）：**
- 在同一时间段内处理多个任务
- 可能在单核CPU上通过时间片轮转实现
- asyncio属于并发编程

**并行（Parallelism）：**
- 在同一时刻真正同时执行多个任务
- 需要多核CPU支持
- 多进程、多线程可以实现真正的并行

### 1.4 为什么需要异步编程

1. **提高程序效率**：在等待I/O操作时可以执行其他任务
2. **更好的资源利用**：避免线程阻塞，减少资源浪费
3. **处理高并发**：单线程处理大量并发连接
4. **响应性更好**：用户界面不会因为后台操作而卡顿

---

## 2. asyncio简介

### 2.1 什么是asyncio

asyncio是Python 3.4版本引入的标准库，用于编写异步I/O操作的代码。它提供了一种高效的方式来处理并发任务，特别适用于I/O密集型操作。

**主要特点：**
- 基于事件循环（Event Loop）
- 使用协程（Coroutine）实现异步操作
- 单线程并发模型
- 内置对网络编程的支持

### 2.2 asyncio的核心组件

1. **事件循环（Event Loop）**：asyncio的核心，负责调度和执行协程
2. **协程（Coroutine）**：可以暂停和恢复的函数
3. **任务（Task）**：对协程的封装，可以被事件循环调度
4. **Future**：表示异步操作的结果

### 2.3 asyncio的工作原理

asyncio采用事件驱动的编程模型：

1. 程序启动一个事件循环
2. 将需要执行的协程注册到事件循环中
3. 事件循环不断检查是否有可执行的协程
4. 当协程遇到await时，控制权返回给事件循环
5. 事件循环继续执行其他可执行的协程
6. 当异步操作完成时，相应的协程被唤醒继续执行

---

## 3. 基础语法和概念

### 3.1 async和await关键字

Python 3.5引入了`async`和`await`关键字，使异步编程更加简洁易读。

**async关键字：**
- 用于定义协程函数
- `async def`定义的函数返回一个协程对象

**await关键字：**
- 用于等待异步操作完成
- 只能在async函数内部使用
- 会暂停当前协程的执行，直到等待的操作完成

### 3.2 协程（Coroutine）

协程是可以暂停和恢复执行的函数。在Python中，使用`async def`定义的函数就是协程函数。

```python
async def my_coroutine():
    print("协程开始执行")
    await asyncio.sleep(1)  # 暂停1秒
    print("协程继续执行")
    return "协程执行完毕"
```

### 3.3 事件循环（Event Loop）

事件循环是asyncio的核心，负责：
- 调度协程的执行
- 处理I/O事件
- 管理回调函数
- 处理信号和异常

### 3.4 任务（Task）

任务是对协程的封装，可以被事件循环调度执行。使用`asyncio.create_task()`可以创建任务。

### 3.5 Future

Future表示异步操作的结果，它是一个占位符，表示将来会有一个值。

---


## 4. 基础代码示例

### 4.1 Hello World示例

让我们从最简单的asyncio程序开始：

```python
import asyncio

async def hello_world():
    print("Hello")
    await asyncio.sleep(1)  # 模拟异步操作
    print("World")

# 运行协程
asyncio.run(hello_world())
```

**输出：**
```
Hello
(等待1秒)
World
```

**解释：**
- `async def`定义了一个协程函数
- `await asyncio.sleep(1)`暂停协程1秒，但不阻塞整个程序
- `asyncio.run()`是Python 3.7+推荐的运行协程的方式

### 4.2 基础协程示例

```python
import asyncio
import time

async def say_after(delay, what):
    await asyncio.sleep(delay)
    print(what)

async def main():
    print(f"开始时间: {time.strftime('%X')}")
    
    # 顺序执行（总共需要3秒）
    await say_after(1, 'hello')
    await say_after(2, 'world')
    
    print(f"结束时间: {time.strftime('%X')}")

asyncio.run(main())
```

**输出：**
```
开始时间: 14:30:00
hello
world
结束时间: 14:30:03
```

### 4.3 并发执行示例

```python
import asyncio
import time

async def say_after(delay, what):
    await asyncio.sleep(delay)
    print(what)

async def main():
    print(f"开始时间: {time.strftime('%X')}")
    
    # 并发执行（总共只需要2秒）
    task1 = asyncio.create_task(say_after(1, 'hello'))
    task2 = asyncio.create_task(say_after(2, 'world'))
    
    # 等待两个任务完成
    await task1
    await task2
    
    print(f"结束时间: {time.strftime('%X')}")

asyncio.run(main())
```

**输出：**
```
开始时间: 14:30:00
hello
world
结束时间: 14:30:02
```

### 4.4 使用asyncio.gather()并发执行

```python
import asyncio
import time

async def fetch_data(name, delay):
    print(f"开始获取 {name} 数据...")
    await asyncio.sleep(delay)
    print(f"{name} 数据获取完成")
    return f"{name} 的数据"

async def main():
    print(f"开始时间: {time.strftime('%X')}")
    
    # 使用gather并发执行多个协程
    results = await asyncio.gather(
        fetch_data("用户信息", 1),
        fetch_data("订单信息", 2),
        fetch_data("商品信息", 1.5)
    )
    
    print("所有数据获取完成:")
    for result in results:
        print(f"  - {result}")
    
    print(f"结束时间: {time.strftime('%X')}")

asyncio.run(main())
```

**输出：**
```
开始时间: 14:30:00
开始获取 用户信息 数据...
开始获取 订单信息 数据...
开始获取 商品信息 数据...
用户信息 数据获取完成
商品信息 数据获取完成
订单信息 数据获取完成
所有数据获取完成:
  - 用户信息 的数据
  - 订单信息 的数据
  - 商品信息 的数据
结束时间: 14:30:02
```

### 4.5 协程函数与普通函数的区别

```python
import asyncio

# 普通函数
def normal_function():
    print("这是一个普通函数")
    return "普通函数的返回值"

# 协程函数
async def coroutine_function():
    print("这是一个协程函数")
    await asyncio.sleep(0.1)
    return "协程函数的返回值"

async def main():
    # 调用普通函数
    result1 = normal_function()
    print(f"普通函数结果: {result1}")
    
    # 调用协程函数
    result2 = await coroutine_function()
    print(f"协程函数结果: {result2}")

asyncio.run(main())
```

### 4.6 创建和管理任务

```python
import asyncio

async def background_task(name, duration):
    print(f"任务 {name} 开始执行")
    await asyncio.sleep(duration)
    print(f"任务 {name} 执行完成")
    return f"任务 {name} 的结果"

async def main():
    # 创建任务
    task1 = asyncio.create_task(background_task("A", 2))
    task2 = asyncio.create_task(background_task("B", 1))
    task3 = asyncio.create_task(background_task("C", 3))
    
    print("所有任务已创建，开始执行...")
    
    # 等待所有任务完成
    results = await asyncio.gather(task1, task2, task3)
    
    print("所有任务完成，结果:")
    for result in results:
        print(f"  {result}")

asyncio.run(main())
```

### 4.7 异常处理

```python
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

asyncio.run(main())
```

---


## 5. 进阶应用

### 5.1 网络编程

#### 5.1.1 HTTP客户端示例

```python
import asyncio
import aiohttp
import time

async def fetch_url(session, url):
    """异步获取URL内容"""
    try:
        async with session.get(url) as response:
            content = await response.text()
            return {
                'url': url,
                'status': response.status,
                'length': len(content)
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
            print(f"✅ {result['url']}: {result['status']}, {result['length']} bytes")

# 运行示例
# asyncio.run(fetch_multiple_urls())
```

#### 5.1.2 TCP服务器示例

```python
import asyncio

async def handle_client(reader, writer):
    """处理客户端连接"""
    addr = writer.get_extra_info('peername')
    print(f"客户端 {addr} 已连接")
    
    try:
        while True:
            # 读取客户端数据
            data = await reader.read(1024)
            if not data:
                break
            
            message = data.decode('utf-8').strip()
            print(f"收到来自 {addr} 的消息: {message}")
            
            # 回显消息
            response = f"服务器收到: {message}\n"
            writer.write(response.encode('utf-8'))
            await writer.drain()
            
    except asyncio.CancelledError:
        pass
    except Exception as e:
        print(f"处理客户端 {addr} 时出错: {e}")
    finally:
        print(f"客户端 {addr} 断开连接")
        writer.close()
        await writer.wait_closed()

async def start_server():
    """启动TCP服务器"""
    server = await asyncio.start_server(
        handle_client, 
        'localhost', 
        8888
    )
    
    addr = server.sockets[0].getsockname()
    print(f"服务器启动在 {addr}")
    
    async with server:
        await server.serve_forever()

# 运行服务器
# asyncio.run(start_server())
```

#### 5.1.3 TCP客户端示例

```python
import asyncio

async def tcp_client():
    """TCP客户端示例"""
    try:
        reader, writer = await asyncio.open_connection(
            'localhost', 8888
        )
        
        # 发送消息
        messages = ["Hello", "World", "AsyncIO", "TCP"]
        
        for message in messages:
            print(f"发送: {message}")
            writer.write(f"{message}\n".encode('utf-8'))
            await writer.drain()
            
            # 读取响应
            response = await reader.readline()
            print(f"收到: {response.decode('utf-8').strip()}")
            
            await asyncio.sleep(1)
        
        # 关闭连接
        writer.close()
        await writer.wait_closed()
        
    except Exception as e:
        print(f"客户端错误: {e}")

# 运行客户端
# asyncio.run(tcp_client())
```

### 5.2 文件IO操作

#### 5.2.1 异步文件读写

```python
import asyncio
import aiofiles
import os

async def write_file_async(filename, content):
    """异步写入文件"""
    async with aiofiles.open(filename, 'w', encoding='utf-8') as f:
        await f.write(content)
    print(f"文件 {filename} 写入完成")

async def read_file_async(filename):
    """异步读取文件"""
    try:
        async with aiofiles.open(filename, 'r', encoding='utf-8') as f:
            content = await f.read()
        print(f"文件 {filename} 读取完成，长度: {len(content)}")
        return content
    except FileNotFoundError:
        print(f"文件 {filename} 不存在")
        return None

async def process_multiple_files():
    """并发处理多个文件"""
    files_data = {
        'file1.txt': '这是第一个文件的内容\n' * 100,
        'file2.txt': '这是第二个文件的内容\n' * 200,
        'file3.txt': '这是第三个文件的内容\n' * 150
    }
    
    # 并发写入文件
    write_tasks = [
        write_file_async(filename, content) 
        for filename, content in files_data.items()
    ]
    await asyncio.gather(*write_tasks)
    
    # 并发读取文件
    read_tasks = [
        read_file_async(filename) 
        for filename in files_data.keys()
    ]
    contents = await asyncio.gather(*read_tasks)
    
    # 清理文件
    for filename in files_data.keys():
        if os.path.exists(filename):
            os.remove(filename)
    
    return contents

# 运行示例
# asyncio.run(process_multiple_files())
```

### 5.3 任务管理和控制

#### 5.3.1 任务取消

```python
import asyncio

async def long_running_task(name, duration):
    """长时间运行的任务"""
    try:
        print(f"任务 {name} 开始执行")
        for i in range(duration):
            await asyncio.sleep(1)
            print(f"任务 {name} 执行中... {i+1}/{duration}")
        print(f"任务 {name} 完成")
        return f"任务 {name} 的结果"
    except asyncio.CancelledError:
        print(f"任务 {name} 被取消")
        raise

async def task_cancellation_example():
    """任务取消示例"""
    # 创建任务
    task1 = asyncio.create_task(long_running_task("A", 5))
    task2 = asyncio.create_task(long_running_task("B", 3))
    task3 = asyncio.create_task(long_running_task("C", 4))
    
    # 等待2秒后取消任务A
    await asyncio.sleep(2)
    task1.cancel()
    
    # 等待剩余任务完成
    results = await asyncio.gather(task1, task2, task3, return_exceptions=True)
    
    print("任务结果:")
    for i, result in enumerate(results, 1):
        if isinstance(result, asyncio.CancelledError):
            print(f"  任务{chr(64+i)}: 已取消")
        elif isinstance(result, Exception):
            print(f"  任务{chr(64+i)}: 异常 - {result}")
        else:
            print(f"  任务{chr(64+i)}: {result}")

# 运行示例
# asyncio.run(task_cancellation_example())
```

#### 5.3.2 任务超时控制

```python
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
# asyncio.run(timeout_example())
```

#### 5.3.3 信号量控制并发数

```python
import asyncio
import random

async def limited_resource_task(semaphore, task_id):
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

# 运行示例
# asyncio.run(semaphore_example())
```

### 5.4 队列和生产者-消费者模式

#### 5.4.1 基础队列示例

```python
import asyncio
import random

async def producer(queue, producer_id):
    """生产者"""
    for i in range(5):
        item = f"Producer-{producer_id}-Item-{i}"
        await queue.put(item)
        print(f"生产者 {producer_id} 生产了: {item}")
        await asyncio.sleep(random.uniform(0.5, 1.5))
    
    # 发送结束信号
    await queue.put(None)
    print(f"生产者 {producer_id} 完成")

async def consumer(queue, consumer_id):
    """消费者"""
    while True:
        item = await queue.get()
        if item is None:
            # 收到结束信号，重新放回队列供其他消费者使用
            await queue.put(None)
            break
        
        print(f"消费者 {consumer_id} 消费了: {item}")
        # 模拟处理时间
        await asyncio.sleep(random.uniform(0.5, 2.0))
        queue.task_done()
    
    print(f"消费者 {consumer_id} 完成")

async def queue_example():
    """队列示例"""
    # 创建队列
    queue = asyncio.Queue(maxsize=5)
    
    # 创建生产者和消费者
    producers = [
        asyncio.create_task(producer(queue, i)) 
        for i in range(1, 3)
    ]
    consumers = [
        asyncio.create_task(consumer(queue, i)) 
        for i in range(1, 4)
    ]
    
    # 等待所有生产者完成
    await asyncio.gather(*producers)
    
    # 等待队列中的所有任务完成
    await queue.join()
    
    # 取消消费者任务
    for c in consumers:
        c.cancel()
    
    print("队列示例完成")

# 运行示例
# asyncio.run(queue_example())
```

---


## 6. 高级特性

### 6.1 自定义事件循环

```python
import asyncio
import threading
import time

class CustomEventLoop:
    """自定义事件循环示例"""
    
    def __init__(self):
        self.loop = asyncio.new_event_loop()
        self.thread = None
    
    def start(self):
        """在新线程中启动事件循环"""
        self.thread = threading.Thread(target=self._run_loop)
        self.thread.start()
    
    def _run_loop(self):
        """运行事件循环"""
        asyncio.set_event_loop(self.loop)
        self.loop.run_forever()
    
    def stop(self):
        """停止事件循环"""
        self.loop.call_soon_threadsafe(self.loop.stop)
        if self.thread:
            self.thread.join()
    
    def run_coroutine(self, coro):
        """在事件循环中运行协程"""
        future = asyncio.run_coroutine_threadsafe(coro, self.loop)
        return future.result()

async def background_task(name, duration):
    """后台任务"""
    print(f"后台任务 {name} 开始")
    await asyncio.sleep(duration)
    print(f"后台任务 {name} 完成")
    return f"任务 {name} 的结果"

def custom_loop_example():
    """自定义事件循环示例"""
    print("=== 自定义事件循环示例 ===")
    
    # 创建自定义事件循环
    custom_loop = CustomEventLoop()
    custom_loop.start()
    
    try:
        # 在自定义循环中运行任务
        result1 = custom_loop.run_coroutine(background_task("A", 1))
        print(f"结果1: {result1}")
        
        result2 = custom_loop.run_coroutine(background_task("B", 2))
        print(f"结果2: {result2}")
        
    finally:
        custom_loop.stop()
    
    print("自定义事件循环示例完成\n")

# 运行示例
# custom_loop_example()
```

### 6.2 协程池和连接池

```python
import asyncio
import random
from typing import List, Callable, Any

class CoroutinePool:
    """协程池"""
    
    def __init__(self, max_workers: int = 10):
        self.max_workers = max_workers
        self.semaphore = asyncio.Semaphore(max_workers)
        self.active_tasks = set()
    
    async def submit(self, coro_func: Callable, *args, **kwargs):
        """提交协程到池中执行"""
        async with self.semaphore:
            task = asyncio.create_task(coro_func(*args, **kwargs))
            self.active_tasks.add(task)
            try:
                result = await task
                return result
            finally:
                self.active_tasks.discard(task)
    
    async def map(self, coro_func: Callable, iterable):
        """批量执行协程"""
        tasks = [
            self.submit(coro_func, item) 
            for item in iterable
        ]
        return await asyncio.gather(*tasks)
    
    async def shutdown(self):
        """关闭协程池"""
        if self.active_tasks:
            await asyncio.gather(*self.active_tasks, return_exceptions=True)

async def worker_task(item_id, processing_time):
    """工作任务"""
    print(f"开始处理项目 {item_id}")
    await asyncio.sleep(processing_time)
    result = f"项目 {item_id} 处理完成"
    print(result)
    return result

async def coroutine_pool_example():
    """协程池示例"""
    print("=== 协程池示例 ===")
    
    # 创建协程池
    pool = CoroutinePool(max_workers=3)
    
    # 准备任务数据
    items = [(i, random.uniform(0.5, 2.0)) for i in range(1, 11)]
    
    start_time = time.time()
    
    # 使用协程池处理任务
    results = await pool.map(
        lambda item: worker_task(item[0], item[1]), 
        items
    )
    
    end_time = time.time()
    
    print(f"所有任务完成，耗时: {end_time - start_time:.2f}秒")
    print(f"处理了 {len(results)} 个项目")
    
    await pool.shutdown()
    print()

# 运行示例
# asyncio.run(coroutine_pool_example())
```

### 6.3 异步上下文管理器

```python
import asyncio
import aiofiles
import tempfile
import os

class AsyncDatabaseConnection:
    """异步数据库连接示例"""
    
    def __init__(self, connection_string):
        self.connection_string = connection_string
        self.connected = False
    
    async def __aenter__(self):
        """异步进入上下文"""
        print(f"连接到数据库: {self.connection_string}")
        await asyncio.sleep(0.1)  # 模拟连接时间
        self.connected = True
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """异步退出上下文"""
        print("关闭数据库连接")
        await asyncio.sleep(0.1)  # 模拟关闭时间
        self.connected = False
        if exc_type:
            print(f"处理异常: {exc_type.__name__}: {exc_val}")
        return False  # 不抑制异常
    
    async def execute(self, query):
        """执行查询"""
        if not self.connected:
            raise RuntimeError("数据库未连接")
        
        print(f"执行查询: {query}")
        await asyncio.sleep(0.2)  # 模拟查询时间
        return f"查询结果: {query}"

class AsyncFileManager:
    """异步文件管理器"""
    
    def __init__(self, filename, mode='w'):
        self.filename = filename
        self.mode = mode
        self.file = None
    
    async def __aenter__(self):
        """异步打开文件"""
        print(f"打开文件: {self.filename}")
        self.file = await aiofiles.open(self.filename, self.mode)
        return self.file
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """异步关闭文件"""
        if self.file:
            await self.file.close()
            print(f"关闭文件: {self.filename}")

async def async_context_manager_example():
    """异步上下文管理器示例"""
    print("=== 异步上下文管理器示例 ===")
    
    # 数据库连接示例
    async with AsyncDatabaseConnection("postgresql://localhost:5432/mydb") as db:
        result1 = await db.execute("SELECT * FROM users")
        print(result1)
        
        result2 = await db.execute("SELECT * FROM orders")
        print(result2)
    
    # 文件操作示例
    temp_file = tempfile.mktemp(suffix='.txt')
    try:
        async with AsyncFileManager(temp_file, 'w') as f:
            await f.write("Hello, Async World!\n")
            await f.write("This is an async file operation.\n")
        
        # 读取文件
        async with AsyncFileManager(temp_file, 'r') as f:
            content = await f.read()
            print(f"文件内容:\n{content}")
    
    finally:
        # 清理临时文件
        if os.path.exists(temp_file):
            os.remove(temp_file)
    
    print()

# 运行示例
# asyncio.run(async_context_manager_example())
```

### 6.4 异步迭代器和生成器

```python
import asyncio
import random

class AsyncRange:
    """异步范围迭代器"""
    
    def __init__(self, start, stop, step=1, delay=0.1):
        self.start = start
        self.stop = stop
        self.step = step
        self.delay = delay
        self.current = start
    
    def __aiter__(self):
        return self
    
    async def __anext__(self):
        if self.current >= self.stop:
            raise StopAsyncIteration
        
        value = self.current
        self.current += self.step
        
        # 模拟异步操作
        await asyncio.sleep(self.delay)
        return value

async def async_data_generator(count, delay=0.1):
    """异步数据生成器"""
    for i in range(count):
        # 模拟数据获取
        await asyncio.sleep(delay)
        data = {
            'id': i,
            'value': random.randint(1, 100),
            'timestamp': asyncio.get_event_loop().time()
        }
        yield data

async def async_iterator_example():
    """异步迭代器示例"""
    print("=== 异步迭代器示例 ===")
    
    # 使用异步范围迭代器
    print("异步范围迭代器:")
    async for num in AsyncRange(1, 6, delay=0.2):
        print(f"  数字: {num}")
    
    print("\n异步数据生成器:")
    async for data in async_data_generator(5, delay=0.1):
        print(f"  数据: {data}")
    
    print()

# 运行示例
# asyncio.run(async_iterator_example())
```

---

## 7. 性能优化

### 7.1 性能监控和分析

```python
import asyncio
import time
import functools
from typing import Dict, List

class AsyncProfiler:
    """异步性能分析器"""
    
    def __init__(self):
        self.stats: Dict[str, List[float]] = {}
    
    def profile(self, name: str):
        """性能分析装饰器"""
        def decorator(func):
            @functools.wraps(func)
            async def wrapper(*args, **kwargs):
                start_time = time.time()
                try:
                    result = await func(*args, **kwargs)
                    return result
                finally:
                    end_time = time.time()
                    duration = end_time - start_time
                    
                    if name not in self.stats:
                        self.stats[name] = []
                    self.stats[name].append(duration)
            
            return wrapper
        return decorator
    
    def get_stats(self) -> Dict[str, Dict[str, float]]:
        """获取统计信息"""
        result = {}
        for name, durations in self.stats.items():
            result[name] = {
                'count': len(durations),
                'total': sum(durations),
                'avg': sum(durations) / len(durations),
                'min': min(durations),
                'max': max(durations)
            }
        return result
    
    def print_stats(self):
        """打印统计信息"""
        print("=== 性能统计 ===")
        stats = self.get_stats()
        for name, data in stats.items():
            print(f"{name}:")
            print(f"  调用次数: {data['count']}")
            print(f"  总耗时: {data['total']:.4f}s")
            print(f"  平均耗时: {data['avg']:.4f}s")
            print(f"  最小耗时: {data['min']:.4f}s")
            print(f"  最大耗时: {data['max']:.4f}s")
            print()

# 全局分析器实例
profiler = AsyncProfiler()

@profiler.profile("fast_operation")
async def fast_operation(data):
    """快速操作"""
    await asyncio.sleep(0.1)
    return data * 2

@profiler.profile("slow_operation")
async def slow_operation(data):
    """慢速操作"""
    await asyncio.sleep(random.uniform(0.5, 1.0))
    return data ** 2

@profiler.profile("network_request")
async def mock_network_request(url):
    """模拟网络请求"""
    await asyncio.sleep(random.uniform(0.2, 0.8))
    return f"Response from {url}"

async def performance_monitoring_example():
    """性能监控示例"""
    print("=== 性能监控示例 ===")
    
    # 执行一些操作
    tasks = []
    
    # 快速操作
    for i in range(10):
        tasks.append(fast_operation(i))
    
    # 慢速操作
    for i in range(5):
        tasks.append(slow_operation(i))
    
    # 网络请求
    urls = [f"https://api.example.com/endpoint{i}" for i in range(8)]
    for url in urls:
        tasks.append(mock_network_request(url))
    
    # 并发执行所有任务
    results = await asyncio.gather(*tasks)
    
    # 打印性能统计
    profiler.print_stats()

# 运行示例
# asyncio.run(performance_monitoring_example())
```

### 7.2 内存优化

```python
import asyncio
import gc
import psutil
import os
from typing import AsyncGenerator

class MemoryMonitor:
    """内存监控器"""
    
    @staticmethod
    def get_memory_usage():
        """获取当前内存使用情况"""
        process = psutil.Process(os.getpid())
        memory_info = process.memory_info()
        return {
            'rss': memory_info.rss / 1024 / 1024,  # MB
            'vms': memory_info.vms / 1024 / 1024,  # MB
        }
    
    @staticmethod
    def print_memory_usage(label=""):
        """打印内存使用情况"""
        usage = MemoryMonitor.get_memory_usage()
        print(f"内存使用 {label}: RSS={usage['rss']:.2f}MB, VMS={usage['vms']:.2f}MB")

async def memory_efficient_generator(size: int) -> AsyncGenerator[int, None]:
    """内存高效的异步生成器"""
    for i in range(size):
        # 模拟数据处理
        await asyncio.sleep(0.001)
        yield i
        
        # 定期触发垃圾回收
        if i % 1000 == 0:
            gc.collect()

async def memory_inefficient_approach(size: int):
    """内存低效的方法（一次性加载所有数据）"""
    data = []
    for i in range(size):
        await asyncio.sleep(0.001)
        data.append(i)
    return data

async def memory_efficient_approach(size: int):
    """内存高效的方法（使用生成器）"""
    results = []
    async for item in memory_efficient_generator(size):
        # 只处理当前项目，不保存所有数据
        if item % 100 == 0:
            results.append(item)
    return results

async def memory_optimization_example():
    """内存优化示例"""
    print("=== 内存优化示例 ===")
    
    size = 10000
    
    # 内存低效方法
    MemoryMonitor.print_memory_usage("开始")
    
    print("执行内存低效方法...")
    inefficient_result = await memory_inefficient_approach(size)
    MemoryMonitor.print_memory_usage("低效方法完成")
    
    # 清理数据
    del inefficient_result
    gc.collect()
    
    # 内存高效方法
    print("执行内存高效方法...")
    efficient_result = await memory_efficient_approach(size)
    MemoryMonitor.print_memory_usage("高效方法完成")
    
    print(f"高效方法结果数量: {len(efficient_result)}")
    print()

# 运行示例（需要psutil库）
# asyncio.run(memory_optimization_example())
```

---

## 8. 最佳实践

### 8.1 错误处理最佳实践

```python
import asyncio
import logging
from typing import Optional, Any
from contextlib import asynccontextmanager

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AsyncRetry:
    """异步重试装饰器"""
    
    def __init__(self, max_attempts: int = 3, delay: float = 1.0, backoff: float = 2.0):
        self.max_attempts = max_attempts
        self.delay = delay
        self.backoff = backoff
    
    def __call__(self, func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            last_exception = None
            current_delay = self.delay
            
            for attempt in range(self.max_attempts):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    logger.warning(f"尝试 {attempt + 1}/{self.max_attempts} 失败: {e}")
                    
                    if attempt < self.max_attempts - 1:
                        await asyncio.sleep(current_delay)
                        current_delay *= self.backoff
            
            logger.error(f"所有重试尝试失败，抛出最后一个异常")
            raise last_exception
        
        return wrapper

@asynccontextmanager
async def async_error_handler(operation_name: str):
    """异步错误处理上下文管理器"""
    try:
        logger.info(f"开始执行: {operation_name}")
        yield
        logger.info(f"成功完成: {operation_name}")
    except asyncio.CancelledError:
        logger.warning(f"操作被取消: {operation_name}")
        raise
    except Exception as e:
        logger.error(f"操作失败: {operation_name}, 错误: {e}")
        raise

@AsyncRetry(max_attempts=3, delay=0.5)
async def unreliable_operation(success_rate: float = 0.7):
    """不可靠的操作（用于演示重试）"""
    if random.random() > success_rate:
        raise ValueError("操作失败")
    return "操作成功"

async def error_handling_example():
    """错误处理最佳实践示例"""
    print("=== 错误处理最佳实践示例 ===")
    
    # 使用重试装饰器
    try:
        result = await unreliable_operation(success_rate=0.3)
        print(f"重试结果: {result}")
    except Exception as e:
        print(f"重试最终失败: {e}")
    
    # 使用错误处理上下文管理器
    try:
        async with async_error_handler("重要操作"):
            await asyncio.sleep(0.1)
            # 模拟可能的错误
            if random.random() < 0.3:
                raise RuntimeError("随机错误")
            print("重要操作成功完成")
    except Exception:
        print("错误已被处理")
    
    print()

# 运行示例
# asyncio.run(error_handling_example())
```

### 8.2 资源管理最佳实践

```python
import asyncio
import weakref
from typing import Set, Optional

class ResourceManager:
    """资源管理器"""
    
    def __init__(self):
        self._resources: Set[Any] = set()
        self._cleanup_callbacks = []
    
    def register_resource(self, resource, cleanup_callback=None):
        """注册资源"""
        self._resources.add(resource)
        if cleanup_callback:
            self._cleanup_callbacks.append((weakref.ref(resource), cleanup_callback))
    
    async def cleanup_all(self):
        """清理所有资源"""
        print("开始清理资源...")
        
        # 执行清理回调
        for resource_ref, callback in self._cleanup_callbacks:
            resource = resource_ref()
            if resource is not None:
                try:
                    if asyncio.iscoroutinefunction(callback):
                        await callback(resource)
                    else:
                        callback(resource)
                except Exception as e:
                    logger.error(f"清理资源时出错: {e}")
        
        self._resources.clear()
        self._cleanup_callbacks.clear()
        print("资源清理完成")

class ManagedResource:
    """托管资源示例"""
    
    def __init__(self, name: str, manager: ResourceManager):
        self.name = name
        self.manager = manager
        self.active = True
        
        # 注册到资源管理器
        manager.register_resource(self, self._cleanup)
        print(f"创建资源: {name}")
    
    async def _cleanup(self, resource):
        """清理资源"""
        if resource.active:
            print(f"清理资源: {resource.name}")
            resource.active = False

async def resource_management_example():
    """资源管理最佳实践示例"""
    print("=== 资源管理最佳实践示例 ===")
    
    manager = ResourceManager()
    
    try:
        # 创建一些资源
        resources = [
            ManagedResource(f"Resource-{i}", manager)
            for i in range(5)
        ]
        
        # 模拟使用资源
        await asyncio.sleep(0.1)
        print("资源使用完毕")
        
    finally:
        # 确保资源被清理
        await manager.cleanup_all()
    
    print()

# 运行示例
# asyncio.run(resource_management_example())
```

### 8.3 代码组织最佳实践

```python
import asyncio
from abc import ABC, abstractmethod
from typing import Protocol, runtime_checkable

@runtime_checkable
class AsyncProcessor(Protocol):
    """异步处理器协议"""
    
    async def process(self, data: Any) -> Any:
        """处理数据"""
        ...

class BaseAsyncService(ABC):
    """异步服务基类"""
    
    def __init__(self, name: str):
        self.name = name
        self._running = False
    
    async def start(self):
        """启动服务"""
        if self._running:
            raise RuntimeError(f"服务 {self.name} 已经在运行")
        
        print(f"启动服务: {self.name}")
        self._running = True
        await self._on_start()
    
    async def stop(self):
        """停止服务"""
        if not self._running:
            return
        
        print(f"停止服务: {self.name}")
        await self._on_stop()
        self._running = False
    
    @abstractmethod
    async def _on_start(self):
        """服务启动时的处理"""
        pass
    
    @abstractmethod
    async def _on_stop(self):
        """服务停止时的处理"""
        pass
    
    @property
    def is_running(self) -> bool:
        return self._running

class DataProcessingService(BaseAsyncService):
    """数据处理服务"""
    
    def __init__(self, processor: AsyncProcessor):
        super().__init__("DataProcessingService")
        self.processor = processor
        self.queue = asyncio.Queue()
        self.worker_task: Optional[asyncio.Task] = None
    
    async def _on_start(self):
        """启动工作任务"""
        self.worker_task = asyncio.create_task(self._worker())
    
    async def _on_stop(self):
        """停止工作任务"""
        if self.worker_task:
            self.worker_task.cancel()
            try:
                await self.worker_task
            except asyncio.CancelledError:
                pass
    
    async def _worker(self):
        """工作循环"""
        try:
            while True:
                data = await self.queue.get()
                try:
                    result = await self.processor.process(data)
                    print(f"处理完成: {data} -> {result}")
                except Exception as e:
                    print(f"处理失败: {data}, 错误: {e}")
                finally:
                    self.queue.task_done()
        except asyncio.CancelledError:
            print("工作任务被取消")
            raise
    
    async def submit(self, data: Any):
        """提交数据处理"""
        if not self.is_running:
            raise RuntimeError("服务未运行")
        await self.queue.put(data)

class SimpleProcessor:
    """简单处理器实现"""
    
    async def process(self, data: Any) -> Any:
        """处理数据"""
        await asyncio.sleep(0.1)  # 模拟处理时间
        return data * 2

async def code_organization_example():
    """代码组织最佳实践示例"""
    print("=== 代码组织最佳实践示例 ===")
    
    # 创建处理器和服务
    processor = SimpleProcessor()
    service = DataProcessingService(processor)
    
    try:
        # 启动服务
        await service.start()
        
        # 提交一些数据
        for i in range(5):
            await service.submit(i)
        
        # 等待处理完成
        await service.queue.join()
        
    finally:
        # 停止服务
        await service.stop()
    
    print()

# 运行示例
# asyncio.run(code_organization_example())
```

---


## 9. 常见问题和解决方案

### 9.1 常见错误和解决方法

#### 9.1.1 "RuntimeError: This event loop is already running"

**问题描述：**
在已经运行的事件循环中尝试调用`asyncio.run()`。

**错误示例：**
```python
import asyncio

async def main():
    # 错误：在事件循环中调用asyncio.run()
    await asyncio.run(some_coroutine())  # 这会报错

asyncio.run(main())
```

**解决方案：**
```python
import asyncio

async def main():
    # 正确：直接await协程
    await some_coroutine()

asyncio.run(main())
```

#### 9.1.2 忘记使用await

**问题描述：**
调用协程函数但忘记使用`await`关键字。

**错误示例：**
```python
async def fetch_data():
    await asyncio.sleep(1)
    return "data"

async def main():
    # 错误：忘记await
    result = fetch_data()  # 这返回的是协程对象，不是结果
    print(result)  # 输出: <coroutine object fetch_data at 0x...>

asyncio.run(main())
```

**解决方案：**
```python
async def main():
    # 正确：使用await
    result = await fetch_data()
    print(result)  # 输出: data

asyncio.run(main())
```

#### 9.1.3 在同步函数中调用异步函数

**问题描述：**
在普通函数中尝试调用异步函数。

**错误示例：**
```python
def sync_function():
    # 错误：不能在同步函数中直接await
    result = await async_function()  # SyntaxError
    return result
```

**解决方案：**
```python
def sync_function():
    # 方案1：使用asyncio.run()
    result = asyncio.run(async_function())
    return result

# 方案2：使用asyncio.create_task()和事件循环
def sync_function_with_loop():
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(async_function())
    return result
```

### 9.2 性能陷阱

#### 9.2.1 CPU密集型任务

**问题：**
asyncio适合I/O密集型任务，对CPU密集型任务效果不佳。

**示例：**
```python
import asyncio
import time

async def cpu_intensive_task(n):
    """CPU密集型任务（不适合asyncio）"""
    start = time.time()
    # 计算密集型操作
    result = sum(i * i for i in range(n))
    end = time.time()
    print(f"CPU任务完成，耗时: {end - start:.2f}秒")
    return result

async def io_intensive_task(delay):
    """I/O密集型任务（适合asyncio）"""
    start = time.time()
    await asyncio.sleep(delay)
    end = time.time()
    print(f"I/O任务完成，耗时: {end - start:.2f}秒")
    return f"I/O结果"

async def performance_comparison():
    """性能对比示例"""
    print("=== 性能对比示例 ===")
    
    # CPU密集型任务（并发执行但没有性能提升）
    print("执行CPU密集型任务...")
    start_time = time.time()
    cpu_tasks = [cpu_intensive_task(1000000) for _ in range(3)]
    await asyncio.gather(*cpu_tasks)
    cpu_time = time.time() - start_time
    print(f"CPU密集型任务总耗时: {cpu_time:.2f}秒\n")
    
    # I/O密集型任务（并发执行有显著性能提升）
    print("执行I/O密集型任务...")
    start_time = time.time()
    io_tasks = [io_intensive_task(1) for _ in range(3)]
    await asyncio.gather(*io_tasks)
    io_time = time.time() - start_time
    print(f"I/O密集型任务总耗时: {io_time:.2f}秒")

# 运行示例
# asyncio.run(performance_comparison())
```

#### 9.2.2 阻塞操作

**问题：**
在异步函数中使用阻塞操作会影响整个事件循环。

**错误示例：**
```python
import time
import requests  # 同步HTTP库

async def bad_async_function():
    # 错误：使用阻塞操作
    time.sleep(1)  # 阻塞整个事件循环
    response = requests.get('https://httpbin.org/delay/1')  # 阻塞操作
    return response.json()
```

**解决方案：**
```python
import asyncio
import aiohttp

async def good_async_function():
    # 正确：使用非阻塞操作
    await asyncio.sleep(1)  # 非阻塞延迟
    
    async with aiohttp.ClientSession() as session:
        async with session.get('https://httpbin.org/delay/1') as response:
            return await response.json()

# 或者使用线程池执行阻塞操作
async def async_function_with_thread_pool():
    loop = asyncio.get_event_loop()
    
    # 在线程池中执行阻塞操作
    result = await loop.run_in_executor(
        None,  # 使用默认线程池
        lambda: requests.get('https://httpbin.org/delay/1').json()
    )
    return result
```

### 9.3 调试技巧

#### 9.3.1 启用asyncio调试模式

```python
import asyncio
import warnings

# 启用asyncio调试模式
asyncio.set_event_loop_policy(asyncio.DefaultEventLoopPolicy())
loop = asyncio.new_event_loop()
loop.set_debug(True)
asyncio.set_event_loop(loop)

# 或者在运行时启用
# python -X dev your_script.py

async def debug_example():
    """调试示例"""
    print("调试模式已启用")
    
    # 这会在调试模式下产生警告
    await asyncio.sleep(0.1)
    
    # 忘记await的协程会被检测到
    async def forgotten_coroutine():
        await asyncio.sleep(0.1)
        return "result"
    
    # 这会产生警告（协程未被await）
    coro = forgotten_coroutine()
    del coro  # 删除未await的协程

# 运行示例
# asyncio.run(debug_example())
```

---

## 10. 实际项目应用

### 10.1 Web爬虫

```python
import asyncio
import aiohttp
import time
from urllib.parse import urljoin, urlparse
from typing import Set, List

class AsyncWebCrawler:
    """异步网络爬虫"""
    
    def __init__(self, max_concurrent=10, delay=1.0):
        self.max_concurrent = max_concurrent
        self.delay = delay
        self.session = None
        self.visited_urls: Set[str] = set()
        self.semaphore = asyncio.Semaphore(max_concurrent)
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def fetch_url(self, url: str) -> dict:
        """获取单个URL"""
        if url in self.visited_urls:
            return {'url': url, 'status': 'skipped', 'reason': 'already_visited'}
        
        async with self.semaphore:
            try:
                self.visited_urls.add(url)
                
                async with self.session.get(url) as response:
                    content = await response.text()
                    
                    result = {
                        'url': url,
                        'status': 'success',
                        'status_code': response.status,
                        'content_length': len(content),
                        'title': self._extract_title(content)
                    }
                    
                    print(f"✅ {url} - {response.status} - {len(content)} bytes")
                    
                    # 添加延迟以避免过于频繁的请求
                    await asyncio.sleep(self.delay)
                    
                    return result
                    
            except Exception as e:
                result = {
                    'url': url,
                    'status': 'error',
                    'error': str(e)
                }
                print(f"❌ {url} - {e}")
                return result
    
    def _extract_title(self, html: str) -> str:
        """提取HTML标题"""
        try:
            start = html.lower().find('<title>')
            if start == -1:
                return "No title"
            start += 7
            end = html.lower().find('</title>', start)
            if end == -1:
                return "No title"
            return html[start:end].strip()
        except:
            return "No title"
    
    async def crawl_urls(self, urls: List[str]) -> List[dict]:
        """爬取多个URL"""
        tasks = [self.fetch_url(url) for url in urls]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # 处理异常结果
        processed_results = []
        for result in results:
            if isinstance(result, Exception):
                processed_results.append({
                    'status': 'error',
                    'error': str(result)
                })
            else:
                processed_results.append(result)
        
        return processed_results

async def web_crawler_example():
    """网络爬虫示例"""
    print("=== 异步网络爬虫示例 ===")
    
    urls = [
        'https://httpbin.org/delay/1',
        'https://httpbin.org/delay/2',
        'https://httpbin.org/json',
        'https://httpbin.org/html',
        'https://httpbin.org/xml'
    ]
    
    start_time = time.time()
    
    async with AsyncWebCrawler(max_concurrent=3, delay=0.5) as crawler:
        results = await crawler.crawl_urls(urls)
    
    end_time = time.time()
    
    print(f"\n爬取完成，总耗时: {end_time - start_time:.2f}秒")
    print(f"成功: {sum(1 for r in results if r.get('status') == 'success')}")
    print(f"失败: {sum(1 for r in results if r.get('status') == 'error')}")
    print()

# 运行示例
# asyncio.run(web_crawler_example())
```

### 10.2 异步API服务器

```python
import asyncio
import json
from typing import Dict, Any, Callable
from urllib.parse import parse_qs, urlparse

class AsyncHTTPServer:
    """简单的异步HTTP服务器"""
    
    def __init__(self, host='localhost', port=8080):
        self.host = host
        self.port = port
        self.routes: Dict[str, Callable] = {}
        self.server = None
    
    def route(self, path: str):
        """路由装饰器"""
        def decorator(handler):
            self.routes[path] = handler
            return handler
        return decorator
    
    async def handle_request(self, reader, writer):
        """处理HTTP请求"""
        try:
            # 读取请求行
            request_line = await reader.readline()
            if not request_line:
                return
            
            request_line = request_line.decode('utf-8').strip()
            method, path, version = request_line.split(' ')
            
            # 读取请求头
            headers = {}
            while True:
                line = await reader.readline()
                if line == b'\r\n':
                    break
                if line:
                    key, value = line.decode('utf-8').strip().split(':', 1)
                    headers[key.strip().lower()] = value.strip()
            
            # 解析路径和查询参数
            parsed_url = urlparse(path)
            path = parsed_url.path
            query_params = parse_qs(parsed_url.query)
            
            # 路由处理
            if path in self.routes:
                handler = self.routes[path]
                response_data = await handler(method, query_params, headers)
            else:
                response_data = {
                    'error': 'Not Found',
                    'path': path
                }
                status = '404 Not Found'
            
            # 构建响应
            if isinstance(response_data, dict):
                response_body = json.dumps(response_data, ensure_ascii=False)
                content_type = 'application/json'
                status = '200 OK'
            else:
                response_body = str(response_data)
                content_type = 'text/plain'
                status = '200 OK'
            
            response = (
                f"HTTP/1.1 {status}\r\n"
                f"Content-Type: {content_type}; charset=utf-8\r\n"
                f"Content-Length: {len(response_body.encode('utf-8'))}\r\n"
                f"Connection: close\r\n"
                f"\r\n"
                f"{response_body}"
            )
            
            writer.write(response.encode('utf-8'))
            await writer.drain()
            
        except Exception as e:
            print(f"处理请求时出错: {e}")
        finally:
            writer.close()
            await writer.wait_closed()
    
    async def start(self):
        """启动服务器"""
        self.server = await asyncio.start_server(
            self.handle_request,
            self.host,
            self.port
        )
        
        addr = self.server.sockets[0].getsockname()
        print(f"服务器启动在 http://{addr[0]}:{addr[1]}")
        
        async with self.server:
            await self.server.serve_forever()

# 创建服务器实例
app = AsyncHTTPServer()

@app.route('/')
async def home(method, query_params, headers):
    """首页处理器"""
    return {
        'message': 'Welcome to Async HTTP Server',
        'method': method,
        'timestamp': asyncio.get_event_loop().time()
    }

@app.route('/api/data')
async def api_data(method, query_params, headers):
    """API数据处理器"""
    # 模拟异步数据获取
    await asyncio.sleep(0.1)
    
    return {
        'data': [
            {'id': 1, 'name': 'Item 1'},
            {'id': 2, 'name': 'Item 2'},
            {'id': 3, 'name': 'Item 3'}
        ],
        'query_params': query_params,
        'total': 3
    }

@app.route('/api/slow')
async def slow_endpoint(method, query_params, headers):
    """慢速端点"""
    delay = float(query_params.get('delay', ['1'])[0])
    await asyncio.sleep(delay)
    
    return {
        'message': f'Delayed response after {delay} seconds',
        'delay': delay
    }

async def api_server_example():
    """API服务器示例"""
    print("=== 异步API服务器示例 ===")
    print("启动服务器...")
    print("访问 http://localhost:8080/ 查看首页")
    print("访问 http://localhost:8080/api/data 查看API数据")
    print("访问 http://localhost:8080/api/slow?delay=2 测试慢速端点")
    print("按 Ctrl+C 停止服务器")
    
    try:
        await app.start()
    except KeyboardInterrupt:
        print("\n服务器已停止")

# 运行服务器
# asyncio.run(api_server_example())
```

### 10.3 实时数据处理系统

```python
import asyncio
import json
import random
import time
from typing import Dict, List, Callable
from collections import deque

class RealTimeDataProcessor:
    """实时数据处理系统"""
    
    def __init__(self, buffer_size=1000):
        self.buffer_size = buffer_size
        self.data_buffer = deque(maxlen=buffer_size)
        self.subscribers: List[Callable] = []
        self.running = False
        self.stats = {
            'processed': 0,
            'errors': 0,
            'start_time': None
        }
    
    def subscribe(self, callback: Callable):
        """订阅数据更新"""
        self.subscribers.append(callback)
    
    async def start(self):
        """启动数据处理系统"""
        if self.running:
            return
        
        self.running = True
        self.stats['start_time'] = time.time()
        
        # 启动数据生成器和处理器
        await asyncio.gather(
            self._data_generator(),
            self._data_processor(),
            self._stats_reporter()
        )
    
    async def stop(self):
        """停止数据处理系统"""
        self.running = False
    
    async def _data_generator(self):
        """数据生成器"""
        while self.running:
            try:
                # 生成模拟数据
                data = {
                    'timestamp': time.time(),
                    'sensor_id': random.randint(1, 10),
                    'temperature': random.uniform(20, 35),
                    'humidity': random.uniform(40, 80),
                    'pressure': random.uniform(1000, 1020)
                }
                
                self.data_buffer.append(data)
                await asyncio.sleep(0.1)  # 每100ms生成一条数据
                
            except Exception as e:
                print(f"数据生成错误: {e}")
                self.stats['errors'] += 1
    
    async def _data_processor(self):
        """数据处理器"""
        while self.running:
            try:
                if self.data_buffer:
                    # 批量处理数据
                    batch_size = min(10, len(self.data_buffer))
                    batch = [self.data_buffer.popleft() for _ in range(batch_size)]
                    
                    # 处理数据
                    processed_data = await self._process_batch(batch)
                    
                    # 通知订阅者
                    for callback in self.subscribers:
                        try:
                            if asyncio.iscoroutinefunction(callback):
                                await callback(processed_data)
                            else:
                                callback(processed_data)
                        except Exception as e:
                            print(f"订阅者回调错误: {e}")
                    
                    self.stats['processed'] += len(batch)
                
                await asyncio.sleep(0.05)  # 处理间隔
                
            except Exception as e:
                print(f"数据处理错误: {e}")
                self.stats['errors'] += 1
    
    async def _process_batch(self, batch: List[Dict]) -> Dict:
        """处理数据批次"""
        # 模拟数据处理时间
        await asyncio.sleep(0.01)
        
        # 计算统计信息
        temperatures = [item['temperature'] for item in batch]
        humidities = [item['humidity'] for item in batch]
        
        return {
            'batch_size': len(batch),
            'avg_temperature': sum(temperatures) / len(temperatures),
            'avg_humidity': sum(humidities) / len(humidities),
            'timestamp': time.time(),
            'sensor_count': len(set(item['sensor_id'] for item in batch))
        }
    
    async def _stats_reporter(self):
        """统计报告器"""
        while self.running:
            await asyncio.sleep(5)  # 每5秒报告一次
            
            if self.stats['start_time']:
                runtime = time.time() - self.stats['start_time']
                rate = self.stats['processed'] / runtime if runtime > 0 else 0
                
                print(f"统计信息 - 处理: {self.stats['processed']}, "
                      f"错误: {self.stats['errors']}, "
                      f"速率: {rate:.2f} 条/秒, "
                      f"缓冲区: {len(self.data_buffer)}")

# 数据订阅者示例
async def data_subscriber(processed_data):
    """数据订阅者"""
    print(f"收到处理结果: 批次大小={processed_data['batch_size']}, "
          f"平均温度={processed_data['avg_temperature']:.2f}°C")

def alert_subscriber(processed_data):
    """告警订阅者"""
    if processed_data['avg_temperature'] > 30:
        print(f"⚠️  高温告警: {processed_data['avg_temperature']:.2f}°C")

async def real_time_processing_example():
    """实时数据处理示例"""
    print("=== 实时数据处理系统示例 ===")
    
    # 创建处理器
    processor = RealTimeDataProcessor()
    
    # 添加订阅者
    processor.subscribe(data_subscriber)
    processor.subscribe(alert_subscriber)
    
    try:
        # 运行10秒
        await asyncio.wait_for(processor.start(), timeout=10)
    except asyncio.TimeoutError:
        print("示例运行完成")
    finally:
        await processor.stop()
    
    print()

# 运行示例
# asyncio.run(real_time_processing_example())
```

---

## 总结

Python的asyncio库为异步编程提供了强大而灵活的工具集。通过本教程，我们学习了：

1. **基础概念**：异步编程的原理、事件循环、协程等核心概念
2. **基础语法**：async/await关键字的使用方法
3. **进阶应用**：网络编程、文件IO、任务管理等实际应用场景
4. **高级特性**：自定义事件循环、协程池、异步上下文管理器等
5. **性能优化**：性能监控、内存优化等技巧
6. **最佳实践**：错误处理、资源管理、代码组织等经验
7. **实际应用**：Web爬虫、API服务器、实时数据处理等完整项目

### 关键要点

- **适用场景**：asyncio最适合I/O密集型任务，对CPU密集型任务效果有限
- **性能优势**：在处理大量并发I/O操作时能显著提升性能
- **学习曲线**：需要理解异步编程的思维模式，避免常见陷阱
- **生态系统**：有丰富的异步库支持，如aiohttp、aiofiles等

### 进一步学习建议

1. 深入学习事件循环的内部机制
2. 探索更多异步库和框架（如FastAPI、aiohttp等）
3. 学习异步编程的设计模式
4. 实践更复杂的异步应用项目
5. 关注asyncio的最新发展和最佳实践

通过不断实践和学习，您将能够熟练运用asyncio构建高性能的异步应用程序。

---

*本教程涵盖了Python asyncio的核心概念和实际应用，希望能帮助您掌握异步编程的精髓。*

