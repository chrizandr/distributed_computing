"""Simulator."""
import multiprocessing
from random import randint
import sys

processes = []


class SimProcess(multiprocessing.Process):
    """Simulation of a Processor."""

    def __init__(self, id_, message_queue=[], num_process=1, marker=""):
        """Init."""
        multiprocessing.Process.__init__(self)
        # assert marker in ["L0", "L1", "R0", "R1"]
        assert id_ > 0
        self.pid = id_
        self.messages = message_queue
        self.num_process = num_process
        num = randint((0, 2*num_process))
        self.value = num
        # self.marker = marker

    def receive(self):
        """Receive wait."""
        counter = 0
        while True:
            if not self.messages:
                for message in messages
                message = self.messages
                counter += 1


    def run(self):
        """Sorting logic."""
        prev_ = self.id_ + 1 if self.id_ < self.num_process-1 else -1
        next_ = self.id_ - 1 if self.id_ > 0 else -1
        for i in range(self.num_process):
            if self.id_ % 2 == i % 2:
                network_send(Message(self.value, self.id_, prev_, i))
                network_send(Message(self.value, self.id_, next_, i))
                self.receive()

        return


class Message():
    """Message class."""

    def __init__(self, value, from_id, to_id, round_):
        """Init."""
        self.value = value
        # self.marker = marker
        self.from_id = from_id
        self.to_id = to_id
        self.round = round_


if __name__ == '__main__':

    num_process = int(sys.argv[1])
    tasks = multiprocessing.JoinableQueue()
    results = multiprocessing.Queue()

    left_process = SimProcess(0, Queue(), num_process)
    processes.append(left_process)
    processes.extend([SimProcess(i+1, Queue(), num_process)
                      for i in range(num_process - 2)])
    right_process = SimProcess(num_process-1, Queue(), num_process)
    processes.append(right_process)
