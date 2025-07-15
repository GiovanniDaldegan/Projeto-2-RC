
# ideia. usar essas classes pra ir adicionando roteadores e switchs e hosts até
# a gnt ter uma rede em topologia de árvore

# a gnt teria um menu poder escolher um host pra controlar. dele a gnt pode
# mandar mensagens ICMP de mentirinha de ping e traceroute. daí nosso host manda
# a mensagem pro switch (informando IPs origem e destino), que decide se manda
# pra outro host ou se sobe pra um roteador. depois o roteador escolhe tbm se
# sobe ou desce na rede, sempre com base no IP destino

# aí vamo ter q definir oq cada dispositivo vai fzr quando recebe msg (responde,
# só encaminha, descarta) e como o nosso host printa oq ele recebe
# ainda vou pesquisar mlr pra saber oq rola no traceroute

# obs: tô pensando em fzr algo mais parecido com o processo real, mas a gnt pode
# simplificar por conta do tempo


# root
# a1             a2
# e1     e2      e3     e4
# h1 h2  h3 h4   h5 h6  h7 h8

from time import sleep
from funcs import *


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

        print("src:", bits2cidr(msg.src), "dest:", bits2cidr(msg.dest), msg.time, msg.content)

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
                print(bits2cidr(self.addr))
            else:
                print(bits2cidr(self.left.addr)[:-1] + "1")

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
