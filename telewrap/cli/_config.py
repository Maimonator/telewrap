from functools import partial

import click

# Options
option = partial(click.option, show_default=True)
required = partial(option, required=True)
optional = partial(option, required=False)
