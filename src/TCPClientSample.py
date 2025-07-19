import asyncio


async def tcp_echo_client():
    """
    一个简单的交互式 asyncio TCP 客户端。
    """
    print("正在尝试连接到服务器...")
    try:
        # 1. 使用 open_connection 连接服务器
        #    它返回一个 reader 和 writer，与服务器端的回调函数参数一致
        reader, writer = await asyncio.open_connection(
            'localhost', 8888)
    except ConnectionRefusedError:
        print("连接失败！请确保服务器脚本正在运行。")
        return

    print("已连接到服务器！可以开始发送消息了。")
    print("输入 'exit' 来关闭连接。")

    try:
        while True:
            # 2. 获取用户输入（注意：在真实的GUI或Web应用中，应使用非阻塞方式）
            message = input(">>> ")
            if message.lower() == 'exit':
                break

            # 3. 将消息编码后发送给服务器
            print(f"发送消息: {message!r}")
            writer.write(message.encode('utf-8'))
            # 确保消息被立即发送出去
            await writer.drain()

            # 4. 从服务器读取响应数据
            # 由于服务器总是在响应后加一个 '\n'，用 readline 非常合适
            response = await reader.readline()
            if not response:
                print("服务器关闭了连接。")
                break

            # 5. 解码并打印响应
            print(f"收到响应: {response.decode('utf-8').strip()!r}")

    except Exception as e:
        print(f"发生错误: {e}")
    finally:
        # 6. 关闭连接
        print("正在关闭连接...")
        writer.close()
        await writer.wait_closed()
        print("连接已关闭。")


if __name__ == '__main__':
    try:
        asyncio.run(tcp_echo_client())
    except KeyboardInterrupt:
        print("\n客户端已退出。")