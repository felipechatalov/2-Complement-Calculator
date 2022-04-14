_BITS = 16
_MAX_INT_SIZE = 2 ** (_BITS-1) - 1

# soma +
# subtracao -
# multi. *
# div. /


def decToBin(n: int):
    # separado em partes caso 1 linha seja confuso

    # coloca o sinal, 0 para positivo e 1 para negativo
    # p1 = ("0" if n > 0 else "1")
   
    # completa o numero com "0" ate o numero desejado de bits
    # p2 = "0" * (_BITS - (len(toBinary(n)))-1)
   
    # transforma um numero inteiro e decimal em binario
    # p3 = toBinary(n)
   
    # apos isso, junta tudo em um string de tamanaho _BITS
    t = toBinary(n)
    r = ("0" * (_BITS - len(t) )  ) + t
    if n >= 0:
        return r
    return c2(r)

# funcao recursiva para converter de binario para decimal
def bd_rec(n: str, i: int):
   
    # pega o bit da iteracao atual e ve se esta ativo ou nao
    # p1 = int(n[i])
   
    # se o bit estiver ativo, soma 2**(i-1) ao numero binario, (i-1 ja que o primeiro bit eh de sinal)
    # p2 = (2**(_BITS-i-1))
   
    # caso o sinal seja negativo, multiplica por -1
    # p3 = (-1 if n[0] == "1" else 1)

    # por fim soma este numero com a proxima chamada recursiva com i+=1
    t = int(n[i]) * (2**(len(n)-i-1)) * (-1 if n[0] == "1" else 1)
    # quando chegamos no bit 1, retorna o ultimo numero sem chamada recursiva pois o ultimo bit eh de sinal
    if (i == len(n)-1):
        return t
    return t + bd_rec(n, i+1)

# chamada da funcao recursiva acima, para que n seja necessario passar o 'i' como parametro
def binToDec(n):
    if n[0] == "0":
        return bd_rec(n, 1)
    return -bd_rec(c2(n), 1)


# funcao para transformar um numero inteiro em binario
# ex: 37 -> 10101
def toBinary(n):
    n = abs(int(n))
    hold = ""
    while n > 0:
        # divide o numero por 2 e pega o resto para a string hold
        b = n//2
        hold += str(n%2)
        n = b
    # retorna a string hold invertida
    return hold[::-1]

# faz a soma de 2 numeros binarios, excluindo sinal
def sum(n1: str, n2: str, co: int, i: int) -> str:
    # t recebe a soma de n1 e n2 e o co(carry out da soma anterior)
    # para a soma eh usado 2 portas XOR
    # print(n1, n2)
    
    if len(n2) < len(n1):
        n2 = ("0" * (len(n1) - len(n2))) + n2
    t = str(int(n1[i]) ^ int(n2[i]) ^ int(co))
   
    # 0 ^ 0 = 0
    # 0 ^ 1 = 1
    # 1 ^ 0 = 1
    # 1 ^ 1 = 0
    if i == 0:
        return t
   
    # o terceiro parametro (carry out) precisa ser 1 se 2 ou mais dos numeros forem 1, caso contrario v recebe 0    
    # 1 1 0 OR 1 0 1 OR 0 1 1 OR 1 1 1
   

    # v = 1 if int(n1[i]) == 1 and int(n2[i]) == 1 and co == 0 or int(n1[i]) == 1 and int(n2[i]) == 0 and co == 1 or int(n1[i]) == 0 and int(n2[i]) == 1 and co == 1 or int(n1[i]) == 1 and int(n2[i]) == 1 and co == 1 else 0
    # por fim retorna a soma de i-1 + a iteracao atual

    return sum(n1, n2, 1 if (int(n1[i]) + int(n2[i]) + int(co)) > 1 else 0, i-1) + t

def absGreater(n1: str, n2: str):
    if n1[0] == "1":
        n1 = c2(n1)
    if n2[0] == "1":
        n2 = c2(n2)

    i = 1
    # incrementa o i ate os bits serem diferentes
    while i < _BITS and n1[i] == n2[i] :
        i += 1
    # caso i chegue ao final quer dizer que o numero eh igual
    if i == _BITS:
        return False
    # caso o bit de n1 for 1 retorna true, pois ele eh maior, se nao, retorna false
    if n1[i] == "1":
        return True
    return False
   

def bitshift(n, b, dir):
    # retorna o numero n deslocado para a direita ou esquerda 'b' bits
    if dir == "right":
        return ("0"*b) + n[:-b]
    return n[b:] + ("0"*b)

def c2(n):
    nr = [""] * len(n)
    for i in range(len(n)):
        nr[i] = "0" if n[i] == "1" else "1"
       
    return sum("".join(nr), decToBin(1), 0, len(n)-1)
   
def sub(n1, n2, co, i):
    return sum(n1, c2(n2), co, i)

def mulOperator(n1, n2):
    a = '0'*_BITS
    q1 = '0'
    q = n1
    m = n2
    count = _BITS
    while count != 0:
        # print(f'{a} {q} {q1} {m}')
        if q[-1] == '0' and q1 == '1':
            # print('somo')
            a = sum(a, m, 0, _BITS-1)
        elif q[-1] == '1' and q1 == '0':
            # print('subtraiu')
            a = sub(a, m, 0, _BITS-1)
            # print("a: ", a)

        full = bitshift(a+q+q1, 1, "right")
        a = full[:_BITS]
        if a[1] == '1':
            a = list(a)
            a[0] = '1'
            a = "".join(a)
        q = full[_BITS:-1]
        q1 = full[-1]
        count -= 1
        # print(f'dps {a} {q} {q1} {m} i: {count}')
    return a+q

# TODO: nao utliza isnal aparentemente
def divOperator(n1, n2):
    a = '0'*_BITS
    q = n1
    m = n2
    count = _BITS
    while count != 0:
        print(f'{a} {q} {m}')
        full = bitshift(a+q, 1, "left")
        a = full[:_BITS]
        q = full[_BITS:]
        a = sub(a, m, 0, _BITS-1)
        if a[0] == '1':
            q = list(q)
            q[-1] = '0'
            q = "".join(q)
            a = sum(a, m, 0, _BITS-1)
        else:
            q = list(q)
            q[-1] = '1'
            q = "".join(q)
        count -= 1
    return q, a


def handleInput():
    print("$ digite um numero em base decimal, seguido por uma operacao (+, -, *, /) e outro numero decimal.")
    print("$ ex: '2 * 3' ou digite 'quit' para sair")
    usr = input().split(" ")
    if usr[0] == "quit":
        return 0, "quit", 0
    if len(usr) != 3:
        raise ValueError("Invalid input, ex: 2 * 3")
    if usr[1] not in ["+", "-", "*", "/"]:
        raise ValueError("Invalid operator, ex: +, -, *, /")
    try:
        n1, n2 = int(usr[0]), int(usr[2])
    except:
        raise ValueError("Invalid input, values must be integers")
    if abs(n1) > _MAX_INT_SIZE or abs(n2) > _MAX_INT_SIZE:
        raise ValueError('n1 or n2 exceeded max int size for {_BITS} bits')

    return decToBin(n1), usr[1], decToBin(n2)

def main():
   
   
    n1, op, n2 = handleInput()
    print(n1, op, n2)
   
    while op != "quit":
       
        # print(f'numero 1: {binToDec(n1)}', end='')
        # print(f' \tbinario: {n1}')
        # print(f'numero 2: {binToDec(n2)}', end='')
        # print(f' \tbinario: {n2}')
        print()
        if op == "+":
            r = sum(n1, n2, 0, _BITS-1)
            print('----------------------------------------------------')
            print(f'resultado: {r}, ({binToDec(r)})')
            print('----------------------------------------------------')
        elif op == "-":
            r = sub(n1, n2, 0, _BITS-1)
            print('----------------------------------------------------')
            print(f'resultado: {r}, ({binToDec(r)})')
            print('----------------------------------------------------')
        elif op == "*":
            r = mulOperator(n1, n2)
            print('----------------------------------------------------')
            print(f'resultado: {r}, ({binToDec(r)})')
            # print(len(r))
            print('----------------------------------------------------')
        elif op == "/":
            r, re = divOperator(n1, n2)
            print('----------------------------------------------------')
            print(f'resultado: {r}, resto: {re}  ({binToDec(r), binToDec(re)})')
            print('----------------------------------------------------')

        n1, op, n2 = handleInput()    

 



if __name__ == "__main__":
    main()
