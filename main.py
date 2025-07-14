from classes import *
from utils import *

def menu():
    options = ["Sair", "Iniciar simulador"]

    while True:
        print_banner("Simulador de Rede", "Projeto 2 de Redes de Computadores\nSelecione uma opção", options)
        
        choice = input_choice()


if __name__ == "__main__":
    menu()
