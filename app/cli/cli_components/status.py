from multiprocessing import Process, Queue
from queue import Empty
from time import sleep

from rich.console import Console


class Status:
    def __init__(self):
        self.process = None
        self.queue = Queue()

    def show_status(self, prompt):
        self.process = Process(
            target=self._show_status,
            args=(self.queue, prompt)
        )
        self.process.start()

    @staticmethod
    def _show_status(queue: Queue, status_prompt):
        console = Console()
        with console.status(status_prompt) as status:
            counter = 0
            while True:
                if counter > 75:
                    counter = 1
                else:
                    counter += 1
                status.update(f"[grey74]{status_prompt}{'.' * int(counter / 20)}[/grey74]")
                sleep(0.00001)
                try:
                    queue.get_nowait()
                    break
                except Empty:
                    pass

    def stop_status(self):
        self.queue.put_nowait(True)
        sleep(0.00002)
        self.process.terminate()
