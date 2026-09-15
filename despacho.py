"""SI Code Week 2026 · Desafio 02 · Torneio de Algoritmos

Escreva a função despachar() abaixo. Não mude o nome nem os parâmetros:
os testes de correção chamam a função exatamente assim.

Regras completas: página do Desafio 02 no sistema da SI Code Week.
Python 3.12, só com a biblioteca padrão.
"""

_CHEGA, _SAI, _CANCELA, _DESFAZ = 0, 1, 2 , 3

_PALAVRAS = {"CHEGA": _CHEGA,
             "SAI": _SAI,
             "CANCELA": _CANCELA,
             "DESFAZ": _DESFAZ}
_SIMBOLOS = {"+": _CHEGA,
             ">": _SAI,
             "-": _CANCELA,
             "<": _DESFAZ}

def _analisar(linha):
    """traduz uma linha do log (v1 ou v2) em (operação, código).

    devolve None para linhas em branco, comentários e comandos desconhecidos.
    """
    corte = linha.find("#")
    if corte != -1:                      # comentário no fim da linha ou linha inteira
        linha = linha[:corte]
    partes = linha.split()               # resolve tabs, espaços múltiplos, CRLF
    if not partes:
        return None

    #pega os tokens dos blocos da linha e vê se bate com algum comando (como CHEGA ou SAI)
    
    cabeca = partes[0]
    op = _SIMBOLOS.get(cabeca[0])        # versão 1: +P1, - p1, >, <
    if op is None:
        op = _PALAVRAS.get(cabeca.upper())   # versão 2: CHEGA/SAI/CANCELA/DESFAZ
        if op is None:
            return None                  # comando desconhecido: ignora a linha
        resto = ""
    else:
        resto = cabeca[1:]               # "+P004" -> "P004"; "+" -> ""
    if resto:
        return op, resto.upper()
    if len(partes) > 1:
        return op, partes[1].upper()     # "+ P005" / "CHEGA P005"
    return op, ""                        # ">", "<", "SAI", "DESFAZ"

def despachar(log: list[str]) -> list[str]:
    """Recebe as linhas do log de despacho e devolve os códigos dos pedidos
    entregues, na ordem em que saíram.

    >>> despachar(["CHEGA P1", "CHEGA P2", "SAI"])
    ['P1']
    """
    prox = [0]
    ante = [0]
    codigo_do = [""]
    na_fila = [False]
    no_do = {}
    entregues = []
    desfazer = []

    for linha in log:
        analisado = _analisar(linha)
        if analisado is None:
            continue
        op, codigo = analisado

        if op == _CHEGA:
            if not codigo or codigo in no_do:
                continue
            no = len(codigo_do)
            ultimo = ante[0]
            codigo_do.append(codigo)
            prox.append(0)
            ante.append(ultimo)
            na_fila.append(True)
            prox[ultimo] = no
            ante[0] = no
            no_do[codigo] = no
            desfazer.append(no << 2 | _CHEGA)

        elif op == _SAI:
            no = prox[0]
            if no == 0:
                continue
            seguinte = prox[no]
            prox[0] = seguinte
            ante[seguinte] = 0
            na_fila[no] = False
            entregues.append(codigo_do[no])
            desfazer.append(no << 2 | _SAI)

        elif op == _CANCELA:
            no = no_do.get(codigo)
            if no is None or not na_fila[no]:
                continue
            prox[ante[no]] = prox[no]
            ante[prox[no]] = ante[no]
            na_fila[no] = False
            desfazer.append(no << 2 | _CANCELA)

        else:
            if not desfazer:
                continue
            registro = desfazer.pop()
            no = registro >> 2
            feito = registro & 3
            if feito == _CHEGA:
                prox[ante[no]] = prox[no]
                ante[prox[no]] = ante[no]
                na_fila[no] = False
                del no_do[codigo_do[no]]
            else:
                if feito == _SAI:
                    entregues.pop()
                prox[ante[no]] = no
                ante[prox[no]] = no
                na_fila[no] = True

    return entregues

    
