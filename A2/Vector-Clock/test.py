# Spins variable number of threads to perform variable number of actions each
# Possible actions: do work, leave message, check messages
# Any action increments the thread's vector clock; leaving a message sends a copy of the thread's vector clock; recieving a message updates thread's vector clock with merged result of clock check
# At completion, each mailbox slot contains each thread's final vector clock at the time that thread finished

import clock
from threading import Thread
import random
import time

threads = 5
iterations = 100
mailbox = [None] * threads

class ClockThread(Thread):
    def __init__(self, id):
        super(ClockThread, self).__init__()
        self.id = id
        self.clock = clock.Clock([0] * threads)

    def run(self):
        for i in range(iterations):
            action = random.randint(0,2)
            print()
            if action is 0:
                #do fake work
                time.sleep(0.1)
                self.clock.increment(self.id)
                print("#" + str(self.id) + " does some work! Internal clock = " + str(self.clock))
            elif action is 1:
                #send fake message (can send to self)
                recipient = random.randint(0,threads-1)
                self.clock.increment(self.id)
                msgClock = self.clock
                mailbox[recipient] = msgClock
                print("#" + str(self.id) + " leaves a message for #" + str(recipient) + "! Clock sent = " + str(msgClock) + ", internal clock = " + str(self.clock))
            else:
                #check for & recieve fake message
                if mailbox[self.id] is not None:
                    msgClock = mailbox[self.id]
                    mailbox[self.id] = None
                    self.clock.merge(msgClock, self.id)
                    print("#" + str(self.id) + " collects a message! Clock recieved = " + str(msgClock) + ", internal clock = " + str(self.clock))
                else:
                    self.clock.increment(self.id)
                    print("#" + str(self.id) + " checks messages & finds none! Internal clock = " + str(self.clock))
        mailbox[self.id] = self.clock
        print("#" + str(self.id) + " is done! Internal clock at completion time = " + str(self.clock))

threadlist = []

for i in range(threads):
    t = ClockThread(i)
    threadlist.append(t)

for t in threadlist:
    t.start()

for t in threadlist:
    t.join()

print("Final mailbox values:")
for c in mailbox:
    print(str(c))
