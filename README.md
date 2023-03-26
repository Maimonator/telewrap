# Telewrap

Telewrap is a Python package that can make your life as a developer so much easier.
With this tool, you don't have to constantly check your shell to see if your code has finished compiling or if your model has finished training.
Telewrap sends notifications straight to your telegram, freeing you up to focus on other tasks or take a break, knowing that you'll be alerted as soon as the job is done.

# Getting started

## TLDR
For those of you that just want to make it work:
```bash
pip install telewrap
tl configure # then follow the instructions
tlw sleep 5
```

You can then send `/status` to your bot to get the last line from the `STDOUT` or `STDERR` of the program to your telegram.

## Installation

To install Telewrap, run:

```pip install telewrap```

This will install two command line interfaces: `tl` and `tlw`.

## Configuration

To configure Telewrap, run the following command and follow the printed instructions:

``bash
tl configure
``

By default, the configuration file is saved in the expanded path `~/.config/.telewrap.config`. If you want to save it to a different directory, you can use the environment variable `TELEWRAP_CONFIG_DIR`. For example, the following command will save the configuration file under /tmp/.telewrap.config:

```bash
TELEWRAP_CONFIG_DIR=/tmp tl configure
```

## Usage

### Command line

To wrap a command line program until it finishes and get the result in your Telegram chat, run:

```bash
tlw my_program
```
Now you can send `/status` to your bot to get the last line from the `STDOUT` or `STDERR` of the program to your telegram.

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

The `Telewrap` object is configurable via the `status_func` and `end_func` parameters.
You can override them so you can get a custom message when you send `/status` to your bot, or the program finishes running.
You can see example functions under `telewrap/core/message_funcs.py`.
Note that both of these functions expect to receive a single paramater which is `start_time: datetime.datetime` object.

Here's an example with overriding both the `status_func` and `end_func`

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
Telewrap is a valuable tool that for any task that requires waiting, one example is checking the availability of a website. All you need to do is write a script that checks whether a website is ready or you can use the one in  `examples/is_website_ready.py`.
Then just run:

```bash
tlw python examples/is_website_ready.py https://google.com
```

This will provide you with a notification as soon as the website is available.