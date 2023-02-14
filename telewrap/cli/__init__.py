import importlib
from pathlib import Path

import click


@click.group()
def cli():
    """Telewrap job command-line interface"""
    pass


# Then add a @click.group with call {group_name}
curdir = Path(__file__).parent
sub_clis = [path.stem for path in curdir.iterdir() if '_cli' in path.stem]
for sub_cli in sub_clis:
    pkg = importlib.import_module(f'telewrap.telewrap_cli.{sub_cli}')
    command = getattr(pkg, sub_cli.replace('_cli', ''))
    cli.add_command(command)
