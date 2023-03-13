import asyncio
import json
import threading
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Union

import telegram.constants
from telegram import Update
from telegram.ext import Application, CommandHandler

from telewrap.core.constants import CONFIG_PATH
from telewrap.core.message_funcs import default_end_func, default_status_func
from telewrap.core.raising_thread import RaisingThread
from telewrap.core.singleton import Singleton


@dataclass
class TelewrapConfig(metaclass=Singleton):
    token: str
    users: List[int]

    @classmethod
    def from_file(cls, file_path: Union[str, Path]):
        file_path = Path(file_path)
        if file_path.exists():
            data = json.loads(file_path.read_text())
            return cls(**data)
        else:
            return cls("", list())

    def to_file(self, file_path: Union[str, Path], create_parents=False):
        file_path = Path(file_path)
        if create_parents:
            file_path.parent.mkdir(exist_ok=True, parents=True)
        Path(file_path).write_text(json.dumps(asdict(self), indent=4))


class TelegramBot:
    def __init__(self, stop_event, config_file, token=None, status_func=default_status_func, end_func=default_end_func, configuration_mode=False):
        if token is None and (config_file is None or not config_file.exists()):
            raise RuntimeError(
                "Please configure Telewrap by running `tl configure` before using it")

        self._configuration_mode = configuration_mode
        self._config_file = config_file
        self._config = TelewrapConfig.from_file(config_file)
        if token is not None:
            self._config.token = token

        self._stop_event = stop_event
        self._status_func = status_func
        self._end_func = end_func

        self.app = Application.builder().token(self._config.token).build()
        if self._configuration_mode:
            self.app.add_handler(CommandHandler('start', self._start_cmd))
            self.app.add_handler(CommandHandler('end', self._end_cmd))
        else:
            self.app.add_handler(CommandHandler('status', self._status_cmd))

    async def start(self):
        await self.app.initialize()
        await self.app.updater.start_polling()
        await self.app.start()
        self.start_time = datetime.now()

    async def _broadcast(self, message_func):
        for chat_id in self._config.users:
            await self.app.updater.bot.send_message(chat_id, message_func(self.start_time), parse_mode=telegram.constants.ParseMode.MARKDOWN)

    async def stop(self):
        if not self._configuration_mode:
            await self._broadcast(self._end_func)
        await self.app.updater.stop()
        await self.app.stop()
        await self.app.shutdown()

        self.start_time = None

    async def _status_cmd(self, update: Update, _context: Dict):
        await update.message.reply_text(self._status_func(self.start_time), parse_mode=telegram.constants.ParseMode.MARKDOWN)

    async def _start_cmd(self, update: Update, _context: Dict):
        self._config.users.append(update.message.chat_id)
        self._config.users = list(set(self._config.users))
        self._config.to_file(self._config_file)
        await update.message.reply_text(f"Subscribed to updates! Your chat_id is {update.message.chat_id}.")

    async def _end_cmd(self, update: Update, _context: Dict):
        await update.message.reply_text(f'Ending configuration stage.')
        self._stop_event.set()


class Telewrap:
    def __init__(self, config_file=CONFIG_PATH, status_func=default_status_func, end_func=default_end_func, token=None, configuration_mode=False):
        self._status_func = status_func
        self._end_func = end_func
        self._token = token
        self._config_file = config_file
        self._configuration_mode = configuration_mode
        self._loop = asyncio.new_event_loop()
        self._started_event = threading.Event()

    def _run_bot(self):
        asyncio.set_event_loop(self._loop)
        self._stop_event = asyncio.Event()

        self._bot = TelegramBot(self._stop_event, self._config_file,
                                self._token, self._status_func, self._end_func, self._configuration_mode)
        self._loop.run_until_complete(self._bot.start())
        self._started_event.set()
        self._loop.run_until_complete(self._stop_event.wait())
        self._loop.run_until_complete(self._bot.stop())


    def __enter__(self):
        self._thread = RaisingThread(target=self._run_bot, daemon=True)
        self._thread.start()

        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        if exc_type is not None or not self._configuration_mode:
            self._loop.call_soon_threadsafe(self._stop_event.set)
        self._thread.join()
        self._thread = None
        self._bot = None
        self._stop_event = None
        return exc_type is None
