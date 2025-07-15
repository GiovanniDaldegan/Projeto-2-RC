
def addr2bits(addr:str):
    """
    Converte um endereço 0.0.0.0 em uma string de bits
    """
    if not "." in addr:
        return

    segments = addr.split(".")

    if len(segments) != 4:
        return
    else:
        for i in segments:
            if not i.isnumeric():
                return
            if int(i) > 255:
                return

    bits = ""
    for i in segments:
        bits += f"{str(bin(int(i)))[2:]: >8}".replace(" ", "0")

    return bits


def find_match(bit_strings, dest_addr:str):
    """
    bit_strings: listas com string de bits e interface correspondente
    dest_addr: string de bits do endereço de destino

    retorna a interface junto com a string q dá match
    """

    prev_matchs = []

    for i_bit in range(1, len(dest_addr) + 1):
        matchs = []

        for i_table in range(len(bit_strings)):
            if bit_strings[i_table][:i_bit] == dest_addr[:i_bit]:
                matchs.append(i_table)

        if len(matchs) > 1:
            if i_bit == len(dest_addr):
                return matchs[0]
            prev_matchs = matchs

        elif len(matchs) == 1:
            return matchs[0]

        else:
            if len(prev_matchs) != 0:
                return prev_matchs[0]

            return

# testa match
# print(find_match(["0100", "0111", "0000"], input()))