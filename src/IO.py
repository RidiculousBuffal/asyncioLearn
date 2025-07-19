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
    input("按enter清理内容")
    # 清理文件
    for filename in files_data.keys():
        if os.path.exists(filename):
            os.remove(filename)

    return contents

if __name__ == '__main__':
    asyncio.run(process_multiple_files())