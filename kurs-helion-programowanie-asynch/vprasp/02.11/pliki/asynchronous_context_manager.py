import asyncio
import contextlib
from typing import Iterable


@contextlib.asynccontextmanager
async def read_alternately(file_names: Iterable):
    files = []
    file = 0
    line = 0
    try:
        for file_name in file_names:
            files.append(open(file_name, 'r', encoding='UTF-8'))
        lines = [[line.strip() for line in f.readlines()] for f in files]
        max_lines = max([len(file) for file in lines])
        alternately_lines = []
        while True:
            alternately_lines.append(lines[file][line])
            file += 1
            if file == len(files):
                file = 0
                line += 1
            if line == max_lines:
                break
        yield alternately_lines
    finally:
        for file in files:
            file.close()


async def main():
    async with read_alternately(['plik1.txt', 'plik2.txt']) as result:
        for line in result:
            print(line)

asyncio.run(main())
