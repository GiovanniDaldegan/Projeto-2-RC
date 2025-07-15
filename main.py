from classes import *
from funcs import *
from utils import *

def setup_network():
    host_addresses = [
        "192.168.0.10",
        "192.168.0.11",
        "192.168.0.34",
        "192.168.0.35",
        "192.168.0.66",
        "192.168.0.67",
        "192.168.0.98",
        "192.168.0.99"
    ]

    hosts = []

    for i in range(len(host_addresses)):
        hosts.append(Host(host_addresses[i], 15))

    e1 = Switch("192.168.0.1",  hosts[0], hosts[1], 15)
    e2 = Switch("192.168.0.33", hosts[2], hosts[3], 15)
    e3 = Switch("192.168.0.65", hosts[4], hosts[5], 15)
    e4 = Switch("192.168.0.97", hosts[6], hosts[7], 15)

    a1 = Router(e1, e2, 20, [
        ["192.168.0.10", 0],
        ["192.168.0.11", 0],
        ["192.168.0.34", 1],
        ["192.168.0.35", 1]
    ], "192.168.1.2")

    a2 = Router(e3, e4, 20, [
        ["192.168.0.66", 0],
        ["192.168.0.67", 0],
        ["192.168.0.98", 1],
        ["192.168.0.99", 1]
    ], "192.168.1.6")

    c1 = Router(a1, a2, 35, [
        ["192.168.0.10", 0],
        ["192.168.0.11", 0],
        ["192.168.0.34", 0],
        ["192.168.0.35", 0],
        ["192.168.0.66", 1],
        ["192.168.0.67", 1],
        ["192.168.0.98", 1],
        ["192.168.0.99", 1]
    ])

    # 11000000101010000000000001100011

    e1.set_parent(a1)
    e2.set_parent(a1)
    e3.set_parent(a2)
    e4.set_parent(a2)

    a1.set_parent(c1)
    a2.set_parent(c1)

    return [[c1], [a1, a2], [e1, e2, e3, e4], hosts]


def ping(network):
    while True:
        print_banner("XPing", desc="Escolha um host (1 a 8):")

        host = network[3][input_choice(8) + 1]
        dest = cidr2bits(input("Selecione o endereço IP de destino: "))
        if not is_valid_addr(dest):
            input("Endereço inválido!")
            continue

        content = input("Digite o conteúdo da mensagem: ")

        host.send_message(Message(host.addr, dest, "xping", content))

        leave()
        return


def traceroute(network):
    while True:
        print_banner("XTraceroute", desc="Escolha um host (1 a 8):")

        host = network[3][input_choice(8) + 1]
        dest = cidr2bits(input("Selecione o endereço IP de destino: "))
        if not is_valid_addr(dest):
            input("Endereço inválido!")
            continue

        content = input("Digite o conteúdo da mensagem: ")

        host.send_message(Message(host.addr, dest, "xtraceroute", content))

        leave()
        return


def command_menu():
    options = ["Voltar", "XPing", "XTraceroute"]

    while True:
        print_banner("Simulação", desc="Escolha um comando para simular", options=options)

        choice = input_choice(len(options))

        match (choice):
            case 0:
                return
            case 1:
                ping(setup_network())
            case 2:
                traceroute(setup_network())
            case _:
                invalid_choice()


def menu():
    options = ["Sair", "Iniciar simulador"]

    while True:
        print_banner("Simulador de Rede", "Projeto 2 de Redes de Computadores\nSelecione uma opção", options)

        choice = input_choice(len(options))

        match (choice):
            case 0:
                clear()
                return
            case 1:
                command_menu()
            case _:
                invalid_choice()
                


if __name__ == "__main__":
    menu()
