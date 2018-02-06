"""Simulator."""
import multiprocessing
from random import randint
import sys

processes = []
num_process = 0


def network_send(message, to_id):
    """Send message to to_id."""
    assert to_id <= num_process and to_id >= 0
    processes[to_id].messages.append(message)


class SimProcess(multiprocessing.Process):
    """Simulation of a Processor."""

    def __init__(self, id_):
        """Init."""
        multiprocessing.Process.__init__(self)
        # assert marker in ["L0", "L1", "R0", "R1"]
        assert id_ > 0
        self.pid = id_
        self.messages = []
        self.num_process = -1
        num = randint((0, 2*num_process))
        self.value = num
        self.round = 0
        # self.marker = marker

    def service(self, ms_id):
        """Message service."""
        message = self.message[ms_id]
        if message.type is "Service":
            pass
        elif message.type is "Action":
            pass

    def receive(self, num_messages):
        """Receive wait."""
        counter = 0
        while True:
            if not self.messages:
                for i in range(len(self.messages)):
                    if self.messages[i].round == self.round:
                        counter += 1
                        self.service(i)
                    if counter == num_messages:
                        self.round += 1
                        return None

    def init_process_count(self):
        """Initiate counting of processes."""
        pass

    def run(self):
        """Sorting logic."""
        prev_ = self.id_ + 1 if self.id_ < self.num_process-1 else -1
        next_ = self.id_ - 1 if self.id_ > 0 else -1
        for i in range(1, self.num_process+1):
            if self.id_ % 2 == i % 2:
                network_send(Message(self.value, self.id_, prev_, i))
                network_send(Message(self.value, self.id_, next_, i))
                self.receive()

        return


class Message():
    """Message class."""

    def __init__(self, value, from_id, to_id, round_, type_):
        """Init."""
        self.value = value
        # self.marker = marker
        self.from_id = from_id
        self.to_id = to_id
        self.round = round_
        self.type = type_


if __name__ == '__main__':

    num_process = int(sys.argv[1])
    left_process = SimProcess(0)
    processes.append(left_process)
    processes.extend([SimProcess(i+1) for i in range(num_process - 2)])
    right_process = SimProcess(num_process-1)
    processes.append(right_process)
