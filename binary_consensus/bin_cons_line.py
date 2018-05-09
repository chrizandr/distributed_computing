"""Distributed Binary consensus algorithm."""
import multiprocessing
import math
from multiprocessing import Pipe
from random import randint
import sys
import pdb

legend = ("{}LOG LEGEND{}\n".format('-'*5, '-'*5) +
          "[#]\tIntermediate state\n" +
          ">>\tFinal Result\n" +
          "..\t Communication record\n" +
          "**\t Snapshot of variables\n" +
          "{}----------{}\n".format('-'*5, '-'*5))
processes = []
verbose = False
num_process = -1
e_0 = 1/2.0 - 0.000000001
e_1 = 1/2.0 + 0.000000001


def assign_state(my_state, other_state):
    """Assign the new states."""
    my_new = my_state
    other_new = other_state
    if my_state == 0 and other_state == 1:
        other_new = 0
        my_new = e_1
    elif my_state == 1 and other_state == 0:
        other_new = 1
        my_new = e_0
    elif my_state == e_0 and other_state == 0:
        other_new = e_0
        my_new = 0
    elif my_state == 0 and other_state == e_0:
        other_new = 0
        my_new = e_0
    elif my_state == e_0 and other_state == e_1:
        other_new = e_0
        my_new = e_1
    elif my_state == e_1 and other_state == e_0:
        other_new = e_1
        my_new = e_0
    elif my_state == e_0 and other_state == 1:
        other_new = e_0
        my_new = 1
    elif my_state == 1 and other_state == e_0:
        other_new = 1
        my_new = e_1
    elif my_state == e_1 and other_state == 1:
        other_new = e_1
        my_new = 1
    elif my_state == 1 and other_state == e_1:
        other_new = 1
        my_new = e_1
    elif my_state == 0 and other_state == e_1:
        other_new = 0
        my_new = 0
    elif my_state == e_1 and other_state == 0:
        other_new = e_1
        my_new = e_0

    return my_new, other_new


class SimProcess(multiprocessing.Process):
    """Simulation of a Processor."""

    def __init__(self, id_, l_connection=None, r_connection=None, init_flag=False):
        """Initializes a process by assigning appropriate values to  it."""
        multiprocessing.Process.__init__(self)
        assert id_ >= 0
        self.l_connection = l_connection
        self.r_connection = r_connection
        self.id_ = id_
        self.num_process = num_process
        num = randint(0, 10**4)
        self.state = num % 2
        self.init_flag = init_flag
        self.alpha = [0.0, 0.0]

    def reply_message(self, message):
        """Handle Reply type messages. The sender reads reply messages sent by the receiver."""
        self.state = message.value

    def action_message(self, message):
        """Handle Action type messages. Receiver does local computation on receiving data."""
        my_new, other_new = assign_state(self.state, message.value)
        if message.from_id < self.id_:
            new_message = Message(other_new, self.id_, message.from_id, self.round, "Reply")
            self.l_connection.send(new_message)
            self.state = my_new
        else:
            print("Abort, Wrong message received")
            sys.exit(0)

    def service_message(self, message):
        """Handle Service type messages. These messages are to calculate the value of alpha."""
        next_process = self.id_+1 if message.from_id < self.id_ else self.id_-1
        if message.marker:
            self.alpha = message.value
            message.to_id = next_process
            message.from_id = self.id_
            if self.l_connection is not None:
                print(".. P{} send message to P{}\n".format(self.id_, next_process) if verbose else "", end='')
                self.l_connection.send(message)
        else:
            message.to_id = next_process
            message.from_id = self.id_
            message.value[self.state] += 1
            if self.r_connection is not None:
                print(".. P{} send message to P{}\n".format(self.id_, next_process) if verbose else "", end='')
                self.r_connection.send(message)
            else:
                self.alpha = message.value
                message.to_id = self.id_ - 1
                message.marker = True
                print(".. P{} send message to P{}\n".format(self.id_, self.id_-1) if verbose else "", end='')
                self.l_connection.send(message)

    def handle(self, message):
        """Appropriate message service is called based on the type of the message received."""
        if message.type == "Service":
            self.service_message(message)

        elif message.type == "Action":
            print(".. P{} received Action type message\n".format(self.id_) if verbose else "", end='')
            self.action_message(message)

        elif message.type == "Reply":
            print(".. P{} received Reply type message\n".format(self.id_) if verbose else "", end='')
            self.reply_message(message)

    def receive(self, flag):
        """Process waits for messages from the sender."""
        try:
            assert flag in ["L", "R"]
        except AssertionError:
            self.state = int(self.alpha[0] <= self.alpha[1])
        message = None
        if flag is "L":
            if self.l_connection is not None:
                print(".. P{} waiting for message on left socket.\n".format(self.id_) if verbose else "", end='')
                message = self.l_connection.recv()
                print(".. P{} got message on left socket.\n".format(self.id_) if verbose else "", end='')
                self.handle(message)
        elif flag is "R":
            if self.r_connection is not None:
                print(".. P{} waiting for message on right socket.\n".format(self.id_) if verbose else "", end='')
                message = self.r_connection.recv()
                print(".. P{} got message on right socket.\n".format(self.id_) if verbose else "", end='')
                self.handle(message)

    def find_alpha(self):
        """Initiate finding alpha value."""
        if self.init_flag:
            self.alpha[self.state] += 1
            self.r_connection.send(Message(self.alpha, self.id_, self.id_+1, -1, "Service"))
            self.receive("R")
        else:
            self.receive("L")
            self.receive("R")

    def print_state(self, rounds=None):
        "Print the state of the process."
        if rounds:
            self.receive("l")
            print(" >> P{} state after {} round: {}".format(self.id_, rounds, self.state))
            return None
        if self.state == 0:
            print(" [#] P{} in state: 0".format(self.id_))
        elif self.state == e_0:
            print(" [#] P{} in state: e_0".format(self.id_))
        elif self.state == e_1:
            print(" [#] P{} in state: e_1".format(self.id_))
        elif self.state == 1:
            print(" [#] P{} in state: 1".format(self.id_))

    def run(self):
        """Calls appropriate actions during the whole process of consensus."""
        print(" [...] P{} Value = {}".format(self.id_, self.state))
        self.find_alpha()
        alpha = max(self.alpha)/sum(self.alpha)
        next_ = self.id_ + 1 if self.id_ < self.num_process-1 else -1
        time_p = int(2 * (16 * ((1-alpha)**2) * (self.num_process**2) * math.log(self.num_process)) / (math.pi ** 2))
        i=0
        for i in range(0, time_p):
            self.round = i
            if verbose:
                self.print_state()
            if next_ != -1:
                self.r_connection.send(Message(self.state, self.id_, next_,
                                       i, "Action"))
                print(" .. P{} sent message to right process P{}\n".format(self.id_, next_) if verbose else "", end='')
            if self.id_ != 0:
                self.receive("L")
            if next_ != -1:
                self.receive("R")
            # print(self.state)
        self.print_state(i)


class Message():
    """Message class."""

    def __init__(self, value, from_id, to_id, round_, type_, marker=False):
        """Initialize each message based on the parameters passed."""
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
        print("Usage: python <filename>.py <num_process> <order> [verbose]\n" +
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
