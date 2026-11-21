"""Comparación de configuraciones de SA usada para elegir los parámetros (no se ajustó para balancear clases).
Usa 4 instancias de entrenamiento con n=100 y 4 con n=30; reporta la suma de costos de SA (y de HC como referencia)."""
import os, sys, random
import pandas as pd
sys.path.insert(0, os.path.dirname(__file__))
import tsp_algorithms as A
DATA = os.path.join(os.path.dirname(__file__), "..", "data")
tr = pd.read_csv(os.path.join(DATA, "train.csv"))
ids = list(tr[tr.n == 100].instance_id[:4]) + list(tr[tr.n == 30].instance_id[:4])
CFGS = [dict(T0=0.1, alpha=0.95, iters_factor=10), dict(T0=0.1, alpha=0.98, iters_factor=20), dict(T0=0.05, alpha=0.98, iters_factor=20)]
Ds = []
for i in ids:
    d = pd.read_csv(os.path.join(DATA, "instances", f"{i}.csv")); Ds.append(A.dist_matrix(list(zip(d.x, d.y))))
hc = sum(A.hill_climbing_2opt(D, random.Random(1))[1] for D in Ds)
print(f"HC (referencia): {hc:.3f}")
for cfg in CFGS:
    print(cfg, round(sum(A.simulated_annealing_2opt(D, random.Random(1), **cfg)[1] for D in Ds), 3))
