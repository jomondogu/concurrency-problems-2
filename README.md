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

### Petri Nets
Includes transition.go and transition.py, two competing implementations for the transition feature of a simulated Petri Net.

#### Transition.go
Implements the transition "class" (Golang is not natively object-oriented so this is not strictly a class), which stores number of input channels M, number of output channels N, array inputs storing M input channels, and array outputs storing N output channels. It includes the following functionality:

- (t transition) Eligible(): Returns true if for every input channel of a given transition the max length of the channel (1) equals the current capacity of the channel, and false otherwise.
- (t transition) Fire(): Consumes one token from each input channel and produces one token in each output channel.
- (t transition) Run(): Perpetually fires transition if eligible.

Since Go channels are threadsafe, and since each channel has a buffer of 1, we can safely assume that no channel can ever be overfull, and the transition will only fire when exactly one token appears in every input channel. If any output channel is full at the time of firing, the transition will block by default until the channel is empty, meaning no token will be lost in the mean time. Since Eligible() needs to check each input channel in order, it is possible that a transition may become eligible while the check is already in progress, but in this case the next Eligible() check will discover it anyway. Another possible implementation would involve a flag being tripped when each input channel is filled, and an eligibility flag being tripped once M channel flags are tripped, so that Eligible() would need to check only one value.

#### Transition.py
Implements the transition class, which stores the same variables and includes the same functionality as transition.go, but with the following changes:

- channels are replaced with threadsafe Queues of size 1
- eligible(self) returns false if any input queue is empty, and true otherwise.
- fire(self) removes an item from each input queue and places a 1 in each output queue.

Surprisingly, transition.py is considerably more comprehensible than transition.go, taking precisely half the lines and naturally requiring minimal effort to implement a class with owned variables and methods. The underlying algorithm, however, is exactly the same, and takes advantage of Python's threadsafe Queue object to perform exactly as the channels do in transition.go. Where Python saves space is, as usual, in the syntax for list creation and iteration. It would be possible to save even more space using list comprehension and filtering to check the eligibility condition. In fire(self), the get() and put() functions do not block by default, meaning it would be theoretically possible, absent any other implementation knowledge, for a get() call to return an Empty exception or a put() call to return a Full exception, but this possbility can be eliminated by simply setting the blocking flags to True in both calls.
