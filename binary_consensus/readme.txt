This is the README for the code in this project.

########## DOCUMENTATION ##########
The following are the main classes that are being used along with their methods
and attributes.

SimProcess -> Class representing a process. This inherits from multiprocessing.Process
              Each instance of the class can be run as a seprate process using SimProcess.start()
              Global variables of the parent process become read-only at every instance of the process.

multiprocessing.Pipe -> This is a Communication channel that returns to connector objects.
                        Example: con1, con2 = Pipe(duplex=True)
                        Any picklable Python object can be passed between the two
                        connection objects.
                        In P1: con1.send(obj)
                        In P2: obj = con2.recv()

Message -> This is the message class. This contains only attributes and doesn't contain
           any functions.

SimProcess.run() -> This function contains the loop of the consensus algorithm.
                    In each round, the process sends it's state to the left node.
                    It receives the state from the right node, performs modification
                    according to the algorithm.
                    Replies to the right node. Gets reply from the left node and modifies it's state.

SimProcess.print_state() -> Prints the current state of the process.

SimProcess.find_alpha() -> Finds the value of alpha so as to be able to compute the upper
                           bound on number of rounds.
                           Ideally, alpha should be an estimate and should not be computed
                           using an accumulator.
                           We do this for Simulation purposes.

SimProcess.receive() -> Receives a message on the specified channel and calls the handler to
                        handle the different types of messages.

SimProcess.handle() -> Checks the type of a message and calls the appropriate sub-handler
                       for the message.

SimProcess.service_message() -> Handler for service messages. These are mesages that are
                                used to find the value of alpha.
                                It reads the current value of alpha and updates it
                                according to it's own state before passing it on to the next node.
                                It uses 2N message passing mechanism to compute alpha value.

SimProcess.action_message()  -> Handles action messages. These are messages that are used for the
                                consensus algorithm.
                                It contains the state of the neighbouring node. The states are
                                updated according the algorithm and a "reply" message is sent back.


SimProcess.reply_m 1essage() -> Handle reply type messages. The sender reads reply messages sent by the receiver.

assign_state() -> Finds the next states for the two nodes based on the current state, using the state
                  transition table.


########## USAGE ##########

Usage: python bin_cons_line.py <num_process> <order> [verbose]
num_process : Number of processes to simulate.
verbose : True/False to print the log of the Simulator

Example: python bin_cons_line.py 3 True

Output:
-----LOG LEGEND-----
[#]	Intermediate state
>>	Final Result
..	 Communication record
**	 Snapshot of variables
--------------------

 [...] P0 Value = 1
.. P0 waiting for message on right socket.
 [...] P2 Value = 1
 [...] P1 Value = 1
.. P2 waiting for message on left socket.
.. P1 waiting for message on left socket.
.. P1 got message on left socket.
.. P1 send message to P2
.. P1 waiting for message on right socket.
.. P2 got message on left socket.
.. P2 send message to P1
 [#] P2 in state: 1
.. P1 got message on right socket.
.. P1 send message to P0
 [#] P1 in state: 1
.. P0 got message on right socket.
 [#] P0 in state: 1
