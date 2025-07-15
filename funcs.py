import re

def cidr2bits(addr:str):
    """
    Converte um endereço 0.0.0.0 em uma string de bits
    """

    if is_valid_addr(addr):
        return addr

    if addr.isnumeric():
        if int(addr) > 255 or int(addr) < 0:
            return
        else:
            return f"{str(bin(int(addr)))[2:]: >8}".replace(" ", "0")

    if not "." in addr:
        return

    segments = addr.split(".")

    if len(segments) > 4:
        return
    else:
        for i in segments:
            if not i.isnumeric():
                return
            if int(i) < 0 or int(i) > 255:
                return

    bits = ""
    for i in segments:
        bits += f"{str(bin(int(i)))[2:]: >8}".replace(" ", "0")

    return bits

def bits2cidr(bit_string :str):
    if not bit_string:
        return

    if len(bit_string) != 32:
        return

    cidr_addr = ""
    for i in range(4):
        cidr_addr += f"{int(bit_string[8*i:8*i+8], 2)}."

    return cidr_addr[:-1]

def is_valid_addr(addr):
    if addr:
        if re.fullmatch('[01]+', addr) and len(addr) == 32:
            return True

def find_match(forwarding_table, dest_addr:str):
    """
    forwarding_table: listas com string de bits e interface correspondente
    dest_addr: string de bits do endereço de destino

    retorna a interface junto com a string q dá match
    """


    for i in forwarding_table:
        if i[0] == dest_addr:
            return i[1]

    return -1

    prev_matchs = []

    for i_bit in range(1, len(dest_addr) + 1):
        matchs = []

        for i_table in range(len(forwarding_table)):
            if forwarding_table[i_table][0][:i_bit] == dest_addr[:i_bit]:
                matchs.append(i_table)

        if len(matchs) > 1:
            if i_bit == len(dest_addr):
                return forwarding_table[matchs[0]][1]
            prev_matchs = matchs

        elif len(matchs) == 1:
            return forwarding_table[matchs[0]][1]

        else:
            # se n tá na tabela, não é IP válido na rede
            return -1
            if len(prev_matchs) != 0:
                return forwarding_table[prev_matchs[0]][1]

            return


# deixa pra lá, vou fzr manual msm
def fetch_children_addrs(node, side :int):
    addrs = [node.addr, side]

    if not hasattr(node, "left") or not hasattr(node, "right"):
        return

    addrs.append(*fetch_children_addrs(node.left, side))
    addrs.append(*fetch_children_addrs(node.right, side))

    return addrs

#testa match
#print(find_match([
#    ("001111", 0),
#    ("000111", 0),
#    ("000011", 1),
#    ("000001", 1)
#    ],
#    input()))

# testa tradução CIDR 2 bin
#resultado = cidr2bits(input())
#print(resultado)
#if resultado:
#    print(len(resultado))

# testa tradução bin 2 CIDR
#while True:
#    print(bits2cidr(cidr2bits(input())))

# testa endereço válido
#while True:
#    print(is_valid_addr(input()))