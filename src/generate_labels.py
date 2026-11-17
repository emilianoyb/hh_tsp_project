"""Parte 1: corre los 3 algoritmos en cada instancia y crea train/test etiquetados."""
import os, sys, random, time
from multiprocessing import Pool
import pandas as pd
sys.path.insert(0, os.path.dirname(__file__))
import tsp_algorithms as A

ROOT = os.path.join(os.path.dirname(__file__), "..")
DATA = os.path.join(ROOT, "data")
SEED = 42
NAMES = ["2opt_hill_climbing", "sa_2opt", "mst_2opt"]


def run_instance(iid):
    df = pd.read_csv(os.path.join(DATA, "instances", f"{iid}.csv"))
    pts = list(zip(df.x, df.y))
    D = A.dist_matrix(pts)
    seed = SEED * 100003 + int(iid.split("_")[1])
    c_hc = A.hill_climbing_2opt(D, random.Random(seed))[1]
    c_sa = A.simulated_annealing_2opt(D, random.Random(seed + 1))[1]
    c_mst = A.mst_2opt(D)[1]
    return iid, c_hc, c_sa, c_mst


if __name__ == "__main__":
    t0 = time.time()
    tr = pd.read_csv(os.path.join(DATA, "train.csv"))
    te = pd.read_csv(os.path.join(DATA, "test.csv"))
    ids = list(tr.instance_id) + list(te.instance_id)
    with Pool() as p:
        res = p.map(run_instance, ids, chunksize=4)
    costs = pd.DataFrame(res, columns=["instance_id", "cost_2opt_hill_climbing", "cost_sa_2opt", "cost_mst_2opt"])
    for name, df in (("train", tr), ("test", te)):
        out = df.merge(costs, on="instance_id")
        cc = ["cost_2opt_hill_climbing", "cost_sa_2opt", "cost_mst_2opt"]
        # empates (costos iguales a 1e-9): gana el algoritmo computacionalmente más barato: HC < MST+2opt < SA
        PRIO = {0: 0, 2: 1, 1: 2}
        out["best_algorithm"] = out[cc].apply(lambda r: NAMES[min(range(3), key=lambda k: (round(r.iloc[k], 9), PRIO[k]))], axis=1)
        out.to_csv(os.path.join(DATA, f"{name}_labeled.csv"), index=False)
    print(f"listo en {time.time()-t0:.0f}s")
