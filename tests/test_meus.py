"""Testes adicionais do Desafio 02 — camadas 1, 2 e 3."""
import unittest
import random
from despacho import despachar, _analisar


class TestCasosDeBorda(unittest.TestCase):
    """Camada 1: um caso por regra."""
    
    def test_tudo_ignorado(self):
        self.assertEqual(despachar(["DESFAZ", "SAI", "DESFAZ"]), [])
    
    def test_desfaz_ate_apagar_chegada(self):
        self.assertEqual(
            despachar(["CHEGA P1", "SAI", "DESFAZ", "DESFAZ", "SAI"]),
            []
        )
    
    def test_chegada_volta_possivel_apos_desfaz(self):
        self.assertEqual(
            despachar(["CHEGA P1", "DESFAZ", "CHEGA P1", "SAI"]),
            ["P1"]
        )
    
    def test_cancelado_continua_visto(self):
        self.assertEqual(
            despachar(["CHEGA P1", "CANCELA P1", "CHEGA P1", "SAI"]),
            []
        )
    
    def test_cancela_ignorado_desfaz_pula(self):
        self.assertEqual(
            despachar(["CHEGA P1", "SAI", "CANCELA P1", "DESFAZ", "SAI"]),
            ["P1"]
        )
    
    def test_v1_com_caixa_e_espacos(self):
        self.assertEqual(
            despachar(["chega p1", "\t>", "  <  ", "+P2", "- p1", "DESFAZ", "SAI"]),
            ["P1"]
        )
    
    def test_crlf(self):
        self.assertEqual(
            despachar(["CHEGA P1\r", "SAI\r"]),
            ["P1"]
        )
    
    def test_cabeçalho_e_branco(self):
        self.assertEqual(
            despachar(["#comentario", "   ", "SAI"]),
            []
        )


class TestOraculo(unittest.TestCase):
    """Camada 2: fuzz contra oráculo."""
    
    def _despachar_ingenuo(self, log):
        """Implementação óbvia: guarda estado inteiro a cada operação."""
        fila = []
        entregues = []
        visto = set()
        fotos = []

        for linha in log:
            analisado = _analisar(linha)
            if analisado is None:
                continue
            op, codigo = analisado

            if op == 0:  # _CHEGA
                if not codigo or codigo in visto:
                    continue
                fotos.append((list(fila), list(entregues), set(visto)))
                fila.append(codigo)
                visto.add(codigo)
            elif op == 1:  # _SAI
                if not fila:
                    continue
                fotos.append((list(fila), list(entregues), set(visto)))
                entregues.append(fila.pop(0))
            elif op == 2:  # _CANCELA
                if codigo not in fila:
                    continue
                fotos.append((list(fila), list(entregues), set(visto)))
                fila.remove(codigo)
            elif op == 3:  # _DESFAZ
                if fotos:
                    fila, entregues, visto = fotos.pop()

        return entregues

    def test_20000_logs_aleatorios(self):
        """Fuzz: gera logs aleatórios, compara as duas implementações."""
        random.seed(42)
        codigos = ["P1", "P2", "P3", "p1", "P4"]
        formas = [
            "CHEGA {c}", "chega {c}", "+{c}", "+ {c}",
            "SAI", "sai", ">", "\t> ",
            "CANCELA {c}", "- {c}", "-{c}",
            "DESFAZ", "<", "  <",
            "", "# comentario", "CHEGA {c}   # nota",
            "LIXO {c}"
        ]

        falhas = []
        for rodada in range(20000):
            n = random.randint(1, 40)
            entrada = [
                random.choice(formas).format(c=random.choice(codigos))
                for _ in range(n)
            ]
            rapido = despachar(entrada)
            lento = self._despachar_ingenuo(entrada)
            if rapido != lento:
                falhas.append((entrada, rapido, lento))
                if len(falhas) >= 3:
                    break

        if falhas:
            print("\nDIVERGÊNCIAS:")
            for entrada, rapido, lento in falhas:
                print(f"  entrada: {entrada}")
                print(f"  rapido: {rapido}")
                print(f"  lento:  {lento}")
            self.fail(f"{len(falhas)} divergências encontradas")


if __name__ == "__main__":
    unittest.main()
