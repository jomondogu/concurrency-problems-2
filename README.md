# Concurrency Problems 2
Vector Clocks, Byzantine Generals, and more

### Vector Clocks
Includes clock.py (Clock class implementing simple vector clock) and test.py (test function creating multiple threads to do work, pass messages, and synchronize clocks).

#### Clock.py
Clock.py implements the Clock class, which stores a list representing an individual instance of a vector clock. Clock.py includes the following functionality:

- Increment(self, index): Increments self clock at the given index.
- Compare(self, other): Compares self clock with other clock, returning -1 if self precedes other, 1 if self succeeds other, and 0 if self and other are concurrent or identical. Helper function for concurrent(self,other).
- Concurrent(self,other): Returns true if self and other are concurrent (but not identical), false otherwise.
- Merge(self, other, index): Updates each clock value in self with the maximum value of that clock in self and other, then increments self at the given index.

#### Test.py
Test.py spins a variable number of threads to do a given number of actions, incrementing their own vector clock each time. It also creates an empty list to serve as "mailbox" for the threads to pass messages. Each action is chosen randomly from:

- Do work: Sleep, then increment clock.
- Send message: Choose random thread as recipient, then increment clock and drop copy of clock into mailbox at recipient's index.
- Recieve message: Check mailbox at own index, and if a message exists, merge recieved clock with own clock, then increment clock.

### Byzantine Generals
Includes Byzgen.py.

#### Byzgen.py
Implements the General class, which stores a name, commander boolean, traitor boolean, message queue, and order, and the following functionality:

- Promote(self): Declares self a general.
- Traitorize(self): Declares self a traitor.
- Check_messages(self): Gets next message from self queue.
- Send_message(self, command, other): Puts a message into other queue.
- Random_command(self): Chooses a command at random from "ATTACK" and "RETREAT".
- Traitor_command(self): Changes own order from "ATTACK" to "RETREAT" or vice versa.
- Command(self, command, lieutenants): If self is traitor, sends random command to all lieutenants; otherwise sends command to all lieutenants.
- Pass_on(self, lieutenants): Sends own order to all lieutenants who are not self.
- Get_order(self): Use check_messages(self) to update self order.
- Decide(self): Put all recieved messages into a list, then update self order to the majority command from that list

Currently, the General class is not an extension of the Thread class; however, since Python queues are thread-safe, translating the algorithm to a concurrent environment would not significantly alter its behaviour.

Byzgen.py's main method takes in a recursion level m, number of generals G, number of traitors T, and initial order Oc from the command line. It creates a list of generals, randomly assigns the given number of traitors, and elects a commander (who may be a traitor). It then calls the following test method: 

- Byzantine_generals(generals, m, Oc): If commander is a traitor, it sends random order to each lieutenant; otherwise it sends Oc to each lieutenant. Each lieutenant then checks its given order, and reverses it if it is a traitor. For a number of times equal to the recursion level m, each lieutenant then sends a copy of its given order to all other lieutenants, and decides on a course of action based on the majority order it has recieved from all other lieutenants. For any recursion level greater than 0, this non-concurrent implementation is valid for a number of traitors less than 1/3 of the total generals. A concurrent implementation would not be guaranteed completely valid for any level of recursion since messages could be lost, but a higher level of recursion would prompt a higher likelihood of total agreement.
