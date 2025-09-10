import threading
from typing import Callable, Any, List


class Task:
    def __init__(self, func: Callable, *args: Any, **kwargs: Any):
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def run(self):
        self.func(*self.args, **self.kwargs)


class Queue:
    def __init__(self):
        self.tasks: List[Task] = []

    def add_task(self, func: Callable, *args: Any, **kwargs: Any):
        task = Task(func, *args, **kwargs)
        self.tasks.append(task)

    def run_all(self):
        for task in self.tasks:
            task.run()

    def run_in_background(self):
        thread = threading.Thread(target=self.run_all, daemon=True)
        thread.start()
