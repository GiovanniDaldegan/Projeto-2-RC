from classes import *
from funcs import *
from utils import *

def setup_network():
    host_addresses = [
        "192.168.0.2",
        "192.168.0.3",
        "192.168.0.66",
        "192.168.0.67",
        "192.168.0.130",
        "192.168.0.131",
        "192.168.0.162",
        "192.168.0.163"
    ]

    hosts = []

    for i in range(len(host_addresses)):
        hosts.append(Host(host_addresses[i]))

    e1 = Switch("", hosts[0], hosts[1], 15)
    e2 = Switch("", hosts[2], hosts[3], 15)
    e3 = Switch("", hosts[4], hosts[5], 15)
    e4 = Switch("", hosts[6], hosts[7], 15)

    a1 = Router(e1, "192.168.1.10", e2, "", 20, [("111", ), ("000", )])
    a2 = Router(e3, "", e4, "", 20, [("", ), ("", )])
    c1 = Router(a1, "", a2, "", 35, [])

    return [[c1], [a1, a2], [e1, e2, e3, e4]]


def command_menu():
    options = ["Voltar", "XPing", "XTraceroute"]

    while True:
        print_banner("Simulação", "Escolha um comando para simular", options)

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


def ping(network):
    input(network)
    print_banner("XPing", "Escolha um host (1 a 8):")

    host = input_choice(8)
    dest = addr2bits(input("Selecione o endereço IP de destino: "))

    # mandar msg no switch

    leave()


def traceroute(network):
    print_banner("XTraceroute", "Escolha um host (1 a 8):")

    host = input_choice(8)
    dest = addr2bits(input("Selecione o endereço IP de destino: "))

    # mandar msg no switch

    leave()


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
