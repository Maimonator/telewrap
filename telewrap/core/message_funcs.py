from datetime import datetime
from typing import List

N_LINES_STATUS_MESSAGE = """
```
{lines}
```

{message}
"""

EXCEPTION_END_FAILURE_MESSAGE = """
Task `{command}` failed with error:

```
{exception}
```
{message}
"""

EXCEPTION_END_SUCCESS_MESSAGE = """
Task `{command}` succeeded

{message}
"""


def default_status_func(start_time: datetime) -> str:
    return f"Elapsed time: {str(datetime.now() - start_time)}"


def last_n_lines_status_func(start_time: datetime, lines: List[str], num_lines: int) -> str:
    if len(lines) == 0:
        return default_status_func(start_time)
    else:
        return N_LINES_STATUS_MESSAGE.format(lines="\n".join(lines[-num_lines:]), message=default_status_func(start_time))


def default_end_func(start_time: datetime) -> str:
    return f"Task finished\nElapsed time: {str(datetime.now() - start_time)}"


def exception_end_func(start_time: datetime, command: str, exception: Exception) -> str:
    if exception is None:
        return EXCEPTION_END_SUCCESS_MESSAGE.format(command=command, message=default_status_func(start_time))
    else:
        return EXCEPTION_END_FAILURE_MESSAGE.format(command=command, exception=exception, message=default_status_func(start_time))
