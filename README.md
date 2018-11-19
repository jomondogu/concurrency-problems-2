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
