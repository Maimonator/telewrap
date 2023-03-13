from pathlib import Path
import subprocess
import asyncio

import click
import shlex
import telegram

from telewrap.core import constants
from telewrap.core.message_funcs import last_n_lines_status_func, exception_end_func
from telewrap.core.bot import Telewrap
from telewrap.core.shell_command import run_command

from ._config import optional, required


@click.group
def bot():
    """ Commands for telewrap """


@bot.command(context_settings=dict(ignore_unknown_options=True), no_args_is_help=True)
@click.argument("command", type=click.UNPROCESSED, nargs=-1)
@optional("-n", "--num-lines", help="Number of lines to print in the status command", type=int, default=1)
def wrap(**kwargs):
    """ Wrap a CLI command """
    lines = []
    num_lines = kwargs["num_lines"]
    command = shlex.join(kwargs["command"])
    exception = None

    def status_func(x): return last_n_lines_status_func(x, lines, num_lines)
    def end_func(x): return exception_end_func(x, command, exception)
    with Telewrap(status_func=status_func, end_func=end_func):
        try:
            asyncio.run(run_command(command, lines))
        except subprocess.CalledProcessError as ex:
            exception = ex


@bot.command
@optional("-t", "--token", help="Token to configure the bot with if empty will use previous token", type=str, default=None)
def configure(**kwargs):
    """ Configure telewrap to work with a token """
    print(constants.CONFIGURE_TITLE)
    print(f"Using configuration file: {constants.CONFIG_PATH.absolute()}")
    token = kwargs["token"]
    if token is None:
        print(constants.CONFIGURE_TOKEN)
        token = input("Insert token here: ").strip()
    try:
        constants.CONFIG_PATH.parent.mkdir(exist_ok=True)
        with Telewrap(configuration_mode=True, token=token, config_file=constants.CONFIG_PATH):
            print(constants.CONFIGURE_SUBSCRIPTION)
    except telegram.error.InvalidToken:
        print(constants.CONFIGURE_TOKEN_ERROR.format(token=token))
        return

    print(constants.CONFIGURE_END)
