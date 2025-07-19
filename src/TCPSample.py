import asyncio


async def handle_client(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    addr = writer.get_extra_info('peername')
    print(f'Connection from {addr}')
    try:
        while True:
            data = await reader.read(1024)
            if not data:
                break
            message = data.decode('utf-8').strip()
            response = f'Received {message}\n'
            writer.write(response.encode('utf-8'))
            await writer.drain()
    except asyncio.CancelledError:
        pass
    except Exception as e:
        print(e)
    finally:
        writer.close()
        await writer.wait_closed()


async def start_server():
    server = await asyncio.start_server(handle_client, 'localhost', 8888)
    addr = server.sockets[0].getsockname()
    print(f'Serving on {addr}')
    async with server:
        await server.serve_forever()


if __name__ == '__main__':
    asyncio.run(start_server())
