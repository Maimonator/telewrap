# Telewrap

Telewrap is a Python package for easily sending notifications and reports to your Telegram chat.

# Getting started

## Installation

To install Telewrap, run:

```pip install telewrap```

This will install two command line interfaces: `tl` and `tlw`.

## Configuration

To configure Telewrap, run the following command and follow the instructions:

``bash
tl configure
``

By default, the configuration file is saved in the expanded local directory `~/.config` under the name `.telewrap.config`. If you want to save it to a different directory, you can use the environment variable `TELEWRAP_CONFIG_DIR`. For example, the following command will save the configuration file under /tmp/.telewrap.config:

```bash
TELEWRAP_CONFIG_DIR=/tmp tl configure
```

## Usage

### Command line

To wrap a command line program until it finishes and get the result in your Telegram chat, run:

```bash
tlw my_program
```

If your command has any flags that are conflicting with `tl` you can use the following forms

```bash
tlw -- my_program --help # preferable as it allows for autocomplete
tlw "my_program --help"
```


### In a Python script

It's possible to use telewrap to keep track of the progress when executing lengthy blocks of code.
The following example works in Python scripts and Python notebooks.

```python
from telewrap import Telewrap

with Telewrap():
    while i < 10:
        long_function()
        i += 1
```

If you're using it in code you can even set the status_func and end_func to change the messages so that they fit your needs:

```python
from telewrap import Telewrap, message_funcs
import time

i = 0
def status_func(x): return f"Current iteration {i}\n{message_funcs.default_status_func(x)}" 
def end_func(x): return f"Tada!!" 
with Telewrap(status_func=status_func, end_func=end_func):
    while i < 10:
        # A long function
        time.sleep(1)
        i += 1
```

## Some Useful Examples
Telewrap is a useful tool for checking whether a website is ready for use. You can either write your own script that verifies the website's status or use the provided examples/is_website_ready.py script as a starting point. Once you have your script ready, simply execute the following command in your terminal:

```bash
tlw python is_website_ready.py https://google.com
```

This will provide you with a notification as soon as the website is available.x
