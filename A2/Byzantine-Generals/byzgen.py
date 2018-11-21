#Implements Byzantine Generals algorithm (oral messages) from https://www.microsoft.com/en-us/research/uploads/prod/2016/12/The-Byzantine-Generals-Problem.pdf

import sys
import time
import Queue
import random

class General():

    def __init__(self, name = 0):
        self.name = name
        self.commander = False
        self.messages = Queue.Queue()
        self.traitor = False
        self.order = None

    def promote(self):
        self.commander = True

    def traitorize(self):
        self.traitor = True

    def check_messages(self):
        try:
            message = self.messages.get(True, 1)
            return message
        except Queue.Empty:
            print(str(self) + " recieved no order, defaults to RETREAT")
            return "RETREAT"

    def send_message(self, command, other):
        other.messages.put(command)

    def random_command(self):
        return "ATTACK" if random.randint(0,1) is 0 else "RETREAT"

    def traitor_command(self):
        if self.order == "ATTACK":
            self.order = "RETREAT"
        else:
            self.order = "ATTACK"

    def command(self, command, lieutenants):
        for lieutenant in lieutenants:
            if self.traitor:
                command = self.random_command()
            self.send_message(command, lieutenant)

    def pass_on(self, lieutenants):
        for lieutenant in lieutenants:
            if self.name is not lieutenant.name:
                self.send_message(self.order, lieutenant)

    def get_order(self):
        self.order = self.check_messages()

    def decide(self):
        orders = []
        while not self.messages.empty():
            self.get_order()
            orders.append(self.order)
        print(str(self) + " learned other orders: " + str(orders))
        if len([x for x in orders if x == "ATTACK"]) > len(orders)/2:
            self.order = "ATTACK"
        else:
            self.order = "RETREAT"

    def __str__(self):
        if self.commander:
            return "Commander " + str(self.name) + (" (Traitor)" if self.traitor else "")
        else:
            return "Lieutenant " + str(self.name) + (" (Traitor)" if self.traitor else "")

def byzantine_generals(generals, m, Oc):
    commander = generals[0]
    lieutenants = generals[1:]
    if commander.traitor:
        print("\nCommander is a traitor, sends random commands to all lieutenants")
    else:
        print(str(commander) + " sends " + Oc + " command to all lieutenants")
    commander.command(Oc, lieutenants)
    for lieutenant in lieutenants:
        lieutenant.get_order()
        if lieutenant.traitor:
            lieutenant.traitor_command()
    for i in range(m):
        for lieutenant in lieutenants:
            print(str(lieutenant) + " sends recieved " + lieutenant.order + " command to all other lieutenants")
            lieutenant.pass_on(lieutenants)
        for lieutenant in lieutenants:
            lieutenant.decide()
            print(str(lieutenant) + " decided to " + lieutenant.order)
    decisions = []
    for lieutenant in lieutenants:
        decisions.append(str(lieutenant) + ": " + lieutenant.order)
    if commander.traitor:
        print("\nCommander was a traitor")
    else:
        print ("\nInitial commander order: " + Oc)
    print ("Final lieutenant decisions: " + str(decisions))

m = int(sys.argv[1])
G = int(sys.argv[2])
T = int(sys.argv[3])
Oc = sys.argv[4]

generals = []
for i in range(G):
    generals.append(General(i))
for general in generals[:T]:
    general.traitorize()
random.shuffle(generals)
generals[0].promote()

byzantine_generals(generals, m, Oc)
