from classes import *
from utils import *

def menu():
    options = ["Sair", "Executar Xping", "Executar XTraceroute" ]

    while True:
        print_banner("Projeto 2 - Redes de Computadores", "SIMULADOR DE REDE","Selecione uma opção:\n", options)
        
        choice = input_choice(len(options))


if __name__ == "__main__":
    menu()
