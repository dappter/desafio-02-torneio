import random
import time
from despacho import despachar

# Benchmark 1: Misto realista
print("Benchmark 1: misto realista (200k linhas)")
random.seed(1)
grande = []
for i in range(200_000):
    d = random.random()
    if d < 0.40:
        grande.append(f"CHEGA P{i}")
    elif d < 0.70:
        grande.append("SAI")
    elif d < 0.85:
        grande.append(f"CANCELA P{random.randint(0, i) if i else 0}")
    else:
        grande.append("DESFAZ")

t = time.perf_counter()
saida = despachar(grande)
tempo1 = time.perf_counter() - t

print(f"Tempo: {tempo1:.3f}s, entregues: {len(saida)}")
print(f"Status: {'PASSOU' if tempo1 < 2.0 else 'FALHOU'}")

# Benchmark 2: Adversarial
print("\nBenchmark 2: adversarial (200k linhas)")
random.seed(2)
grande2 = [f"CHEGA P{i}" for i in range(100_000)]
grande2 += ["CANCELA P50000", "DESFAZ"] * 25_000
grande2 += ["SAI"] * 50_000

t = time.perf_counter()
saida2 = despachar(grande2)
tempo2 = time.perf_counter() - t

print(f"Tempo: {tempo2:.3f}s, entregues: {len(saida2)}")
print(f"Status: {'PASSOU' if tempo2 < 2.0 else 'FALHOU'}")

# Resultado
print(f"\nResultado geral: {'PASSOU' if tempo1 < 2.0 and tempo2 < 2.0 else 'FALHOU'}")
