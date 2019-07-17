"""Odd Even transposition sorting implementation."""
import multiprocessing
from multiprocessing import Pipe
from random import randint
import sys
import pdb

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

    def __init__(self, id_, neighbors, incoming_ports):
        """Initialize a process by assigning appropriate values to  it."""
        multiprocessing.Process.__init__(self)
        self.id_ = id_
        self.children = set()
        self.unrelated = set()
        self.neighbors = neighbors  # outgoing ports
        self.incoming_ports = incoming_ports
        self.neighboring_region_ports = set()
        self.x = -1
        self.region_color = -1
        self.parent = -1
        self.universal_color_set = set()
        self.terminated_color_set = set()
        self.neighborhood_color_set = set()
        self.recorded = False

    def record_local_state(self):
        return

    def _forward_message(self, message):
        for connection in self.neighbors:
            if connection:
                connection.send(message)

    def initiate_snap_record(self):
        self.record_local_state()
        self.recorded = True
        self.x = randint(0, 10 ^ 5)
        self.region_color = self.x
        self._forward_message(Message(self.x, "MARKER"))
        self.parent = 'T'
        self.universal_color_set = self.universal_color_set.union({self.x})
        print "Initiate global snapshot for id:", self.id_
        # record_channel_States for all incoming ports to empty set

    def receive_snap_request(self, message, connection_number):
        if not self.recorded:
            self.record_local_state()
            self.recorded = True
            # record incoming port state as empty Cj
            self._forward_message(message)
            self.neighbors[connection_number].send(Message("", "ACCEPT"))
            self.region_color = message.value
            self.universal_color_set = self.universal_color_set.union(message.value)
            self.parent = connection_number
            print "Received snap request, accepted at id:", self.id_
        else:
            self.record_channel_state(connection_number, initial=False)
            self.neighborsp[connection_number].send(Message("", "REJECT"))
            if self.region_color != message.value:
                self.neighborhood_color_set = self.neighborhood_color_set.union({message.value})
                self.neighboring_region_ports = self.neighboring_region_ports.union({connection_number})
            print "Received snap request, rejected at id:", self.id_


    def check_snap_complete(self):
        if self.children.union(self.unrelated) == (self.neighbors - self.parent):
            # node has received a marker on all incoming ports
            self.local_snap_complete()

    def receive_accept(self, connection_number):
        self.children = self.children.union({j})
        self.check_snap_complete()

    def receive_reject(self, connection_number):
        self.unrelated = self.unrelated.union({connection_number})
        self.check_snap_complete()

    def local_snap_complete(self):
        if len(self.children) == 0:
            if self.parent != 'T':
                self.neighbors[self.parent].send(Message(self.neighborhood_color_set, "INSWEEP"))
            else:
                value = [self.x, self.neighborhood_color_set]
                self.neighbors[self.id_].send(Message(value, "TERMINATE"))
        else:
            set1 = {}
            while set1 != self.children:
                for i, each in enumerate(self.incoming_ports):
                    if i in self.children:
                        message = each.recv()
                        print message.type
                        set1.add(message.value)
            if self.parent != 'T':
                self.neighbors[self.parent].send(Message(self.neighborhood_color_set, "INSWEEP"))
            else:
                value = [self.x, self.neighborhood_color_set]
                self.neighbors[self.id_].send(Message(value, "TERMINATE"))

    def receive_terminate(self, message, connection_number):
        x, NCS = message[0], message[1]
        if x not in NCS:
            self.universal_color_set = self.universal_color_set.union(NCS.union({x}))
            self.terminated_color_set = self.terminated_color_set.union({x})
            if self.universal_color_set == self.terminated_color_set:
                print "Snapshots collected and terminated."
            set_ = self.children.union(self.parent.union(self.neighboring_region_ports)) - connection_number
            for each in set_:
                self.neighbors[each].send(Message(message.value, "TERMINATE"))

    def run(self):
        """Call appropriate actions."""
        if self.id_ == 1:
            self.initiate_snap_record()

        for i, connection in enumerate(self.incoming_ports):
            print connection
            message = connection.recv()
            print message.type
            if message.type == "MARKER":
                self.receive_snap_request(message, i)
            elif message.type == "ACCEPT":
                self.receive_accept(i)
            elif message.type == "REJECT":
                self.receive_reject(i)
            elif message.type == "TERMINATE":
                self.receive_terminate(message.value, i)
            else:
                print self.id_, message.type, i


class Message():
    """Message class."""

    def __init__(self, value, type_):
        """Initialize each message based on the parameters passed."""
        self.value = value
        self.type = type_


if __name__ == '__main__':
    if len(sys.argv) > 1:
        num_process = int(sys.argv[1])
        try:
            verbose = bool(sys.argv[2])
        except IndexError:
            pass
    else:
        print("Usage: python <filename>.py <num_process> [verbose]\n" +
              "num_process : Number of processes to simulate.\n" +
              "verbose : True/False to print the log of the Simulator\n")
        sys.exit(0)

    print(legend) if verbose else None

    incoming_connections = [[0 for i in range(num_process)] for j in range(num_process)]
    outgoing_connections = [[0 for i in range(num_process)] for j in range(num_process)]
    print("Enter connections between processes.On completing use '$$' to end stdin.")
    line = raw_input()
    while line != "$$":
        line = line.strip().split("-")
        i, j = int(line[0]), int(line[1])
        connection = Pipe(duplex=True)
        incoming_connections[i][j] = connection[0]
        outgoing_connections[j][i] = connection[0]
        incoming_connections[j][i] = connection[1]
        outgoing_connections[i][j] = connection[1]
        line = raw_input()

    # Create self connections for processes
    for i in range(num_process):
        incoming_connections[i][i], outgoing_connections[i][i] = Pipe(duplex=True)
    # pdb.set_trace()
    # Created processes in a network
    for i in range(num_process):
        processes.append(SimProcess(i, outgoing_connections[i], [incoming_connections[j][i] for j in range(num_process)]))

    # Start all processes.
    for process in processes:
        process.start()
