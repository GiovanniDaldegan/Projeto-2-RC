
def set_link(addr1 :int, addr2 :int, table_ammends, delay_prop :int):
    """
    addr1, addr2  : endereços das interfaces ligadas
    table_ammends : prefixos de endereços adicionais para as tabelas de encaminhamento
    delay_prop    : delay de propagação
    """

    return


def addr2bits(addr:str):
    bits = ""
    for i in addr.split("."):
        bits += bin(i)

    return bits


def find_match(forwarding_table, dest_addr:str):
    # table : [bits string, dest node]
    prev_matchs = []

    for i_bit in range(1, len(dest_addr) + 1):
        matchs = []

        for i_table in range(len(forwarding_table)):
            if forwarding_table[i_table][0][:i_bit] == dest_addr[:i_bit]:
                matchs.append(i_table)
                print(dest_addr[:i_bit], "casa com ", forwarding_table[i_table][0])

        if len(matchs) > 1:
            if i_bit == len(dest_addr):
                print("qualquer um")
                return matchs[0]
            prev_matchs = matchs

        elif len(matchs) == 1:
            print("único")
            return forwarding_table[matchs[0]][1]

        else:
            print('prev', prev_matchs)
            if len(prev_matchs) != 0:
                print("duplicado")
                return forwarding_table[prev_matchs[0]][1]

            return


print(find_match([("0101010", "i1"), ("0101010", "i2"), ("0101111", "i2")], input("addr: ")))
