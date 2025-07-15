import os


def print_banner(title :str=None, subtitle : str=None, desc : str=None, options :list[str]=None):
    if title:
        print("\033[1;34m=" * 150)
        print(f"{title:^150s}")
        print("\033[1;34m=\033[m" * 150)

    if subtitle:
        print("\033[1;32m")
        print(f"{subtitle:^150s}\033[m")

    if desc:
        print(f"\033[1m{desc}\033[m")

    if options:
        for i in range(len(options)):
            print(f"\033[1m[{i}] {options[i]}\033[m")


def clear():
    """Limpa o terminal, tanto no Windows quanto no Linux"""
    os.system('cls' if os.name == 'nt' else 'clear')

def input_choice(n_options:int):
    """
    Considera que o menu vai de 0 a n_options -1

    :param n_options: número de escolhas possíveis

    :returns: -1 se a escolha for inválida
    :returns: valor da escolha se for válida
    """

    choice = input()

    if not choice.isnumeric():
        clear()
        return -1
    
    choice = int(choice)

    if choice < 0 or choice > n_options -1:
        clear()
        return -1

    return choice

