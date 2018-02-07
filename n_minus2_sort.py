"""N minus 2 distrbuted sorting implementation."""
import multiprocessing
from multiprocessing import Pipe
from random import randint
import sys

legend = ("{}LOG LEGEND{}\n".format('-'*5, '-'*5) +
          "-> <-\tSwapping values record\n" +
          ">>\tControl message record\n" +
          "..\t Communication record\n" +
          "**\t Snapshot of variables\n" +
          "{}----------{}\n".format('-'*5, '-'*5))
processes = []
verbose = False


class SimProcess(multiprocessing.Process):
    """Simulation of a Processor."""

    def __init__(self, id_, l_connection=None, r_connection=None, init_flag=False):
        """Init."""
        multiprocessing.Process.__init__(self)
        assert id_ >= 0
        self.l_connection = l_connection
        self.r_connection = r_connection
        self.id_ = id_
        self.num_process = -1
        num = randint(0, 10*num_process)
        self.value = num
        self.round = 0
        self.init_flag = init_flag

    def reply_message(self, message):
        """Handle Reply type messages."""
        self.value = message.value

    def action_message(self, message):
        """Handle Action type messages."""
        if message.value < self.value and message.from_id > self.id_:
            new_message = Message(self.value, self.id_, message.from_id, self.round, "Reply")
            self.value = message.value
            print("-> <- Swapping between P{} and P{}\n".format(self.id_, message.from_id) if verbose else "", end='')
        elif message.value > self.value and message.from_id < self.id_:
            new_message = Message(self.value, self.id_, message.from_id, self.round, "Reply")
            self.value = message.value
            print("-> <- Swapping between P{} and P{}\n".format(self.id_, message.from_id) if verbose else "", end='')
        else:
            new_message = Message(message.value, self.id_, message.from_id, self.round, "Reply")

        if message.from_id < self.id_:
            self.l_connection.send(new_message)
        else:
            self.r_connection.send(new_message)

    def service_message(self, message):
        """Handle Service type messages."""
        next_process = self.id_+1 if message.from_id < self.id_ else self.id_-1
        if message.marker:
            self.num_process = message.value
            message.to_id = next_process
            message.from_id = self.id_
            if self.l_connection is not None:
                print(".. P{} send message to P{}\n".format(self.id_, next_process) if verbose else "", end='')
                self.l_connection.send(message)
        else:
            message.to_id = next_process
            message.from_id = self.id_
            message.value += 1
            if self.r_connection is not None:
                print(".. P{} send message to P{}\n".format(self.id_, next_process) if verbose else "", end='')
                self.r_connection.send(message)
            else:
                self.num_process = message.value
                message.to_id = self.id_ - 1
                message.marker = True
                print(".. P{} send message to P{}\n".format(self.id_, self.id_-1) if verbose else "", end='')
                self.l_connection.send(message)

    def handle(self, message):
        """Message service."""
        if message.type == "Service":
            self.service_message(message)

        elif message.type == "Action":
            print(".. P{} received Action type message\n".format(self.id_) if verbose else "", end='')
            self.action_message(message)

        elif message.type == "Reply":
            print(".. P{} received Reply type message\n".format(self.id_) if verbose else "", end='')
            self.reply_message(message)

    def receive(self, flag):
        """Receive wait."""
        assert flag in ["L", "R"]
        message = None
        if flag is "L":
            if self.l_connection is not None:
                print(".. P{} waiting for message on right socket.\n".format(self.id_) if verbose else "", end='')
                message = self.l_connection.recv()
                print(".. P{} got message on left socket.\n".format(self.id_) if verbose else "", end='')
                self.handle(message)
        elif flag is "R":
            if self.r_connection is not None:
                print(".. P{} waiting for message on right socket.\n".format(self.id_) if verbose else "", end='')
                message = self.r_connection.recv()
                print(".. P{} got message on right socket.\n".format(self.id_) if verbose else "", end='')
                self.handle(message)

    def init_process_count(self):
        """Initiate counting of processes."""
        if self.init_flag:
            self.r_connection.send(Message(1, self.id_, self.id_+1, -1, "Service"))
            self.receive("R")
        else:
            self.receive("L")
            self.receive("R")

    def run(self):
        """Sorting logic."""
        self.init_process_count()
        print("P{} Num process = {}\n".format(self.id_, self.num_process) if verbose else "", end='')

        print("P{} Value = {} at round {}".format(self.id_, self.value, self.round))
        next_ = self.id_ + 1 if self.id_ < self.num_process-1 else -1
        prev_ = self.id_ - 1 if self.id_ > 0 else -1
        for i in range(0, self.num_process-2):
            self.round = i
            print("** P{}: Current Value={} Current round={}\n".format(self.id_, self.value, self.round) if verbose else "", end='')
            if self.id_ % 2 == i % 2:
                print(">> P{} locally computing".format(self.id_) if verbose else "", end='')
                if prev_ != -1:
                    self.l_connection.send(Message(self.value, self.id_, prev_,
                                           i, "Action"))
                    print(" .. P{} sent message to left process P{}\n".format(self.id_, prev_) if verbose else "", end='')
                    self.receive("L")
                if next_ != -1:
                    self.r_connection.send(Message(self.value, self.id_, next_,
                                           i, "Action"))
                    print(" .. P{} sent message to right process P{}\n".format(self.id_, next_) if verbose else "", end='')
                    self.receive("R")
            else:
                self.receive("L")
                self.receive("R")

        print("P{} Value = {} at round {}".format(self.id_, self.value, self.round))


class Message():
    """Message class."""

    def __init__(self, value, from_id, to_id, round_, type_, marker=False):
        """Init."""
        self.value = value
        self.marker = marker
        self.from_id = from_id
        self.to_id = to_id
        self.round = round_
        self.type = type_


if __name__ == '__main__':
    if len(sys.argv) > 1:
        num_process = int(sys.argv[1])
        try:
            verbose = bool(sys.argv[2])
        except IndexError:
            pass
    else:
        print("Usage: python plain_dist_sort.py <num_process> [verbose]\n" +
              "num_process : Number of processes to simulate.\n" +
              "verbose : True/False to print the log of the Simulator\n")
        sys.exit(0)

    print(legend) if verbose else None

    # Create connections for processes to communicate
    connections = [Pipe(duplex=True) for i in range(num_process-1)]

    # Created processes in a line network
    left_process = SimProcess(0, None, connections[0][0], init_flag=True)
    processes.append(left_process)
    processes.extend([SimProcess(i, connections[i-1][1], connections[i][0])
                      for i in range(1, num_process - 1)])
    right_process = SimProcess(num_process-1, connections[num_process-2][1], None)
    processes.append(right_process)

    # Start all processes.
    for process in processes:
        process.start()
