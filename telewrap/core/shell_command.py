import asyncio
import os
import subprocess
import time
from typing import List


class ShellCommand:
    def __init__(self, command):
        if command.startswith("'") and command.endswith("'"):
            self._command = f"/bin/sh -c {command}"
        else:
            self._command = command
        self._process = None
        self._stdout_queue = asyncio.Queue()

    async def __aenter__(self):
        env = os.environ.copy()
        env["PYTHONUNBUFFERED"] = "1"
        self._process = await asyncio.create_subprocess_shell(self._command, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.STDOUT, env=env)
        asyncio.create_task(self._print_lines())
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        await self._process.wait()
        return_code = self._process.returncode
        self._process = None
        if return_code != 0:
            raise subprocess.CalledProcessError(return_code, self._command)

    async def _print_lines(self):
        while True:
            line = await self._process.stdout.readline()
            if not line:
                break
            line = line.decode("utf8").rstrip('\n')
            print(line)
            self._stdout_queue.put_nowait(line)

        await self._stdout_queue.put(None)

    def __aiter__(self):
        return self

    async def __anext__(self):
        line = await self._stdout_queue.get()
        if line is None:
            raise StopAsyncIteration
        return line


async def run_command(command, lines: List[str]):
    async with ShellCommand(command) as sc:
        async for line in sc:
            lines.append(line)
