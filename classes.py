
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


"""
class Interface:
    def __init__(self):

class Link:
    def ___init__(self, l_type, ):
        self.
"""

class ICMPMessage:
    """
    Mensagem ICMP.
    
    type code  desc
    0    0     cmmd ping
    3    0     network unreachable
    3    1     host unreachable
    11   0     cmmd traceroute response?
    """

    def __init__(self, src, dest, m_type, m_code, ttl):
        self.src = src
        self.dest = dest
        self.type = m_type
        self.code = m_code
        self.ttl = ttl

class Router:
    def __init__(self, interfaces):
        self.interfaces = interfaces

    def add_router(self, router):
        """
        Adiciona um link com um roteador
        """
        return

    def add_switch(self, switch):
        """
        Adiciona um link com um switch de borda.
        """

    def forwading(self, message:ICMPMessage):
        """
        Encaminha a mensagem para a devida interface.
        """

        message.ttl -= 1

        return

    def print_forwarding_table(self, interfaces:list=None):
        """
        Imprime tabela de encaminhamento.
        Se interface = None, imprime todas.
        """
        return

class Switch:
    def __init__(self, addr, router_addr):
        self.addr = addr
        self.router_addr = router_addr

    def add_host(self):
        """
        Adiciona um link com um host
        """
        return

class Host:
    def __init__(self, addr, switch_addr):
        self.addr = addr

    # def send_message(self, message:ICMPMessage):
        
