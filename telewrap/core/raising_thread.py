import threading


class RaisingThread(threading.Thread):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._exception = None

    def run(self):
        try:
            if self._target:
                self._target(*self._args, **self._kwargs)
        except Exception as e:
            self._exception = e

    def join(self, timeout=None):
        super().join(timeout)
        if self._exception:
            raise self._exception
