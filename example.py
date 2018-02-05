"""Simulator."""
import multiprocessing
from random import randint
from queue import Queue


class SimProcess(multiprocessing.Process):
    """Simulation of a Processor."""

    def __init__(self, id_, message_queue=None, num_process=1, marker=""):
        """Init."""
        multiprocessing.Process.__init__(self)
        assert marker in ["L", "R"]
        assert id_ > 0
        self.pid = id_
        self.messages = message_queue
        if message_queue is None:
            self.messages = Queue()
        self.num_process = num_process
        num = randint((0, 2*num_process))
        self.storage = [num, num]
        self.marker = marker

    def run(self):
        """Sorting logic."""
        proc_name = self.name
        while True:
            next_task = self.task_queue.get()
            if next_task is None:
                # Poison pill means shutdown
                print '%s: Exiting' % proc_name
                self.task_queue.task_done()
                break
            print '%s: %s' % (proc_name, next_task)
            answer = next_task()
            self.task_queue.task_done()
            self.result_queue.put(answer)
        return


class Message():
    """Message class."""

    def __init__(self, value, marker, from_id, to_id):
        """Init."""
        self.value = value
        self.marker = marker
        self.from_id = from_id
        self.to_id = to_id


if __name__ == '__main__':
    # Establish communication queues
    tasks = multiprocessing.JoinableQueue()
    results = multiprocessing.Queue()

    # Start consumers
    num_consumers = multiprocessing.cpu_count() * 2
    print 'Creating %d consumers' % num_consumers
    consumers = [ Consumer(tasks, results)
                  for i in range(num_consumers) ]
    for w in consumers:
        w.start()

    # Enqueue jobs
    num_jobs = 10
    for i in xrange(num_jobs):
        tasks.put(Task(i, i))

    # Add a poison pill for each consumer
    for i in xrange(num_consumers):
        tasks.put(None)

    # Wait for all of the tasks to finish
    tasks.join()

    # Start printing results
    while num_jobs:
        result = results.get()
        print 'Result:', result
        num_jobs -= 1
