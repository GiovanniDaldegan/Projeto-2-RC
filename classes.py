from time import sleep
from funcs import *
from utils import *

class Message:
    def __init__(self, src:str, dest:str, m_type:str, content):
        self.src = src
        self.dest = cidr2bits(dest)

        self.type = m_type
        self.content = content
        self.time = 0
    
    def add_time(self, time):
        self.time += time


class Host:
    def __init__(self, addr :str, delay :int):
        self.addr = cidr2bits(addr)
        self.delay = delay

    def send_message(self, msg :Message):
        self.parent.get_message(msg)

    def get_message(self, msg :Message):
        msg.add_time(self.delay)

        print(f"src: {bits2cidr(msg.src)}, dest: {bits2cidr(msg.dest)} - {msg.time}ms  {msg.content}")

    def set_parent(self, parent):
        self.parent = parent


class Switch:
    def __init__(self, addr, left_host :Host, right_host :Host, delay :int):
        self.addr = cidr2bits(addr)

        left_host.set_parent(self)
        right_host.set_parent(self)

        self.left = left_host
        self.right = right_host
        self.delay = delay

    def set_parent(self, parent):
        self.parent = parent

    def send_message(self, msg :Message):       # início da simulação
        if msg.dest == self.right.addr:
            self.right.get_message(msg)

        elif msg.dest == self.left.addr:
            self.left.get_message(msg)

        else:
            self.parent.get_message(msg)

    def get_message(self, msg :Message):
        sleep(1)
        msg.add_time(self.delay)

        #print(f"switch {msg.type}, {bits2cidr(self.addr)}")

        #print(bits2cidr(self.left.addr), bits2cidr(self.right.addr), bits2cidr(msg.dest))

        if self.left.addr == msg.dest:
            self.left.get_message(msg)

        elif self.right.addr == msg.dest:
            self.right.get_message(msg)

        else:
            self.parent.get_message(msg)


class Router:
    def __init__(self, left, right, delay, table, addr :str=None):
        self.left = left
        self.right = right

        self.delay = delay

        for i in range(len(table)):
            table[i][0] = cidr2bits(table[i][0])

        self.table = table
        #input(self.table)

        if addr:
            self.addr = cidr2bits(addr)
    
    def print_table(self):
        print("-" * 48)
        print(f"|{"Endereço":^34s}|{"Interface":^11s}|")
        print("-" * 48)
        for i in self.table:
            print(f"|{i[0]:^34s}|{str(i[1]):^11s}|")
            print("-" * 48)

    def set_parent(self, parent):
        self.parent = parent

    def get_message(self, msg :Message):
        sleep(1)
        msg.add_time(self.delay)

        #print(f"router, {msg.type},", end=" ")
        #print(bits2cidr(self.addr) if hasattr(self, 'addr') else "")

        #if not hasattr(self, "addr"):
        #    print("CGEOH")


        if msg.type == "xtraceroute":
            if hasattr(self, "addr"):
                print(bits2cidr(self.addr), end="")
            else:
                print(bits2cidr(self.left.addr)[:-1] + "1", end="")

            print(f" - {msg.time}ms")

        # encaminhamento
        #print(f"encaminhando... destino: {msg.dest} decisão:", find_match(self.table, msg.dest))
        match (find_match(self.table, msg.dest)):
            case 0:
                self.left.get_message(msg)
            case 1:
                self.right.get_message(msg)
            case _:
                if self.parent:
                    self.parent.get_message(msg)
                else:
                    print("Pacote descartado.", msg.content)
