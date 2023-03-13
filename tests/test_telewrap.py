from unittest.mock import MagicMock, patch

import pytest
import telegram

from telewrap import Telewrap, bot, message_funcs


async def async_magic():
    pass

MagicMock.__await__ = lambda x: async_magic().__await__()

@pytest.fixture
def telegram_bot_config_path(tmp_path):
    config_file = tmp_path / "config.json"
    config_file.write_text('{"token": "test_token", "users": []}')
    return config_file


@pytest.fixture
def telegram_bot_stop_event():
    return MagicMock()


@pytest.fixture
def telegram_bot(telegram_bot_stop_event, telegram_bot_config_path):
    with patch("telewrap.bot.Application") as mock_application:
        mock_app = MagicMock()

        mock_app.updater = MagicMock()
        mock_app.updater.bot.send_message = MagicMock()
        mock_application.builder.return_value = mock_application
        mock_application.build.return_value = mock_app

        yield bot.TelegramBot(
            stop_event=telegram_bot_stop_event,
            config_file=telegram_bot_config_path,
            status_func=lambda x: "status",
            end_func=lambda x: "end",
        )


@pytest.fixture
def telewrap_configuration(telegram_bot_config_path):
    with patch("telewrap.bot.Application") as mock_application:
        mock_app = MagicMock()
        mock_app.updater = MagicMock()
        mock_app.updater.bot.send_message = MagicMock()
        mock_application.builder.return_value = mock_app
        telewrap = Telewrap(
            config_file=telegram_bot_config_path,
            status_func=message_funcs.default_status_func,
            end_func=message_funcs.default_end_func,
            token=None,
            configuration_mode=True,
        )
        yield telewrap


@pytest.fixture
def telewrap_regular(telegram_bot_config_path):
    with patch("telewrap.bot.Application") as mock_application:
        mock_app = MagicMock()
        mock_app.updater = MagicMock()
        mock_app.updater.bot.send_message = MagicMock()
        mock_application.builder.return_value = mock_app
        telewrap = Telewrap(
            config_file=telegram_bot_config_path,
            status_func=message_funcs.default_status_func,
            end_func=message_funcs.default_end_func,
            token=None,
            configuration_mode=False,
        )
        yield telewrap


class TestTelegramBot:
    @pytest.mark.asyncio
    async def test_telegram_bot_init(self, telegram_bot, telegram_bot_config_path):
        assert telegram_bot._configuration_mode is False
        assert telegram_bot._config_file == telegram_bot_config_path

    @pytest.mark.asyncio
    async def test_telegram_bot_start(self, telegram_bot):
        with patch("telewrap.bot.datetime") as mock_datetime:
            mock_datetime.now.return_value = "now"
            await telegram_bot.start()
            assert telegram_bot.start_time == "now"

    @pytest.mark.asyncio
    async def test_telegram_bot_stop(self, telegram_bot):
        with patch("telewrap.bot.datetime") as mock_datetime:
            mock_datetime.now.return_value = "now"
            await telegram_bot.start()
            await telegram_bot.stop()
            assert telegram_bot.start_time is None

    @pytest.mark.asyncio
    async def test_telegram_bot_status_cmd(self, telegram_bot):
        update = MagicMock()

        await telegram_bot.start()
        await telegram_bot._status_cmd(update, {})
        update.message.reply_text.assert_called_once_with(
            "status", parse_mode=telegram.constants.ParseMode.MARKDOWN)

    @pytest.mark.asyncio
    async def test_telegram_bot_start_cmd(self, telegram_bot):
        update = MagicMock()
        update.message.chat_id = 6
        telegram_bot._config.to_file = MagicMock()

        await telegram_bot.start()
        await telegram_bot._start_cmd(update, {})

        assert telegram_bot._config.users == [6]
        telegram_bot._config.to_file.assert_called_once_with(
            telegram_bot._config_file)
        update.message.reply_text.assert_called_once_with(
            f"Subscribed to updates! Your chat_id is {update.message.chat_id}."
        )

    @pytest.mark.asyncio
    async def test_telegram_bot_end_cmd(self, telegram_bot):
        update = MagicMock()
        telegram_bot._stop_event.set = MagicMock()

        await telegram_bot.start()
        await telegram_bot._end_cmd(update, {})
        update.message.reply_text.assert_called_once_with("Ending configuration stage.")
        telegram_bot._stop_event.set.assert_called_once()


class TestTelewrap:
    @pytest.mark.timeout(5)
    def test_telewrap_enter_exit_regular_mode(self, telewrap_regular: Telewrap):
        with telewrap_regular as tw:
            thread = tw._thread
            assert True == thread.is_alive()
            tw._started_event.wait()
            event = tw._stop_event
            assert False == event.is_set()

        assert False == thread.is_alive()
        assert True == event.is_set()
        assert None == telewrap_regular._thread
        assert None == telewrap_regular._bot
        assert None == telewrap_regular._stop_event

    @pytest.mark.timeout(5)
    def test_telewrap_enter_exit_configuration_mode(self, telewrap_configuration: Telewrap):
        with telewrap_configuration as tw:
            thread = tw._thread
            assert True == thread.is_alive()

            tw._started_event.wait()
            assert False == tw._stop_event.is_set()
            event = tw._stop_event
            # mimics sending end message
            tw._loop.call_soon_threadsafe(tw._stop_event.set)

        assert True == event.is_set()
        assert False == thread.is_alive()
        assert None == telewrap_configuration._thread
        assert None == telewrap_configuration._bot
        assert None == telewrap_configuration._stop_event
