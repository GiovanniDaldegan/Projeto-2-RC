
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


from funcs import *


class Message:
    def __init__(self, src:str, dest:str, m_type:str):
        self.src = src
        self.dest = dest
        self.type = m_type
        self.time = 0
    
    def add_time(self, time):
        self.time += time


class Host:
    def __init__(self, addr :str):
        self.addr = addr
    
    def get_message(self, msg :Message):
        print(msg.src, msg.dest, msg.time)
    
    def set_parent(self, parent):
        self.parent = parent


class Switch:
    def __init__(self, addr, left_host :Host, right_host :Host, delay :int):
        self.addr = addr

        self.left = left_host
        self.right = right_host
        self.delay = delay

        left_host.parent = self
        right_host.parent = self

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
        msg.add_time(self.delay)

        print("switch", msg.type)

        if self.left.addr == msg.dest:
            self.left.get_message()

        elif self.right.addr == msg.dest:
            self.right.get_message()


class Router:
    def __init__(self, left, left_addr, right, right_addr, delay, table):
        self.left = left
        self.left_addr = left_addr

        self.right_addr = right_addr
        self.right = right

        self.delay = delay
        self.table = table

    def set_parent(self, parent):
        self.parent = parent

    def get_message(self, msg :Message, child):
        msg.add_time(self.delay)

        print("router", msg.type)

        if msg.type == "xtraceroute":
            if child == 0:
                print(self.left_addr)
            else:
                print(self.right_addr)

        # encaminhamento
        # match (find_match(self.table, msg.dest)):
        match (find_match(["010", "011"], "0111")):
            case 0:
                self.left.get_message(msg)
            case 1:
                self.right.get_message(msg)
            case _:
                if self.parent:
                    self.parent.get_message(msg)


