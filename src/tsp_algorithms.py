"""Tres algoritmos para TSP: 2-opt (hill climbing), SA con 2-opt y MST + 2-opt."""
import math
import random

# ---- Parámetros de Recocido Simulado (parte del etiquetado) ----
SA_PARAMS = dict(T0=0.1, Tf=1e-4, alpha=0.98, iters_per_temp_factor=20)  # iters/temp = 20*n


def dist_matrix(pts):
    n = len(pts)
    return [[math.hypot(pts[i][0] - pts[j][0], pts[i][1] - pts[j][1]) for j in range(n)] for i in range(n)]


def tour_cost(tour, D):
    return sum(D[tour[i]][tour[(i + 1) % len(tour)]] for i in range(len(tour)))


def two_opt_delta(tour, D, i, j):
    """Cambio de costo al invertir tour[i+1..j] (0 <= i < j < n)."""
    n = len(tour)
    a, b = tour[i], tour[i + 1]
    c, d = tour[j], tour[(j + 1) % n]
    return D[a][c] + D[b][d] - D[a][b] - D[c][d]


def two_opt_local_search(tour, D):
    """2-opt con mejor mejora por pasada hasta óptimo local."""
    tour = tour[:]
    n = len(tour)
    if n < 4:
        return tour
    improved = True
    while improved:
        improved = False
        best_delta, best_ij = -1e-12, None
        for i in range(n - 1):
            for j in range(i + 2, n):
                if i == 0 and j == n - 1:
                    continue
                dl = two_opt_delta(tour, D, i, j)
                if dl < best_delta:
                    best_delta, best_ij = dl, (i, j)
        if best_ij:
            i, j = best_ij
            tour[i + 1:j + 1] = reversed(tour[i + 1:j + 1])
            improved = True
    return tour


def hill_climbing_2opt(D, rng):
    n = len(D)
    tour = list(range(n))
    rng.shuffle(tour)
    tour = two_opt_local_search(tour, D)
    return tour, tour_cost(tour, D)


def simulated_annealing_2opt(D, rng, T0=None, Tf=None, alpha=None, iters_factor=None):
    p = SA_PARAMS
    T0 = p["T0"] if T0 is None else T0
    Tf = p["Tf"] if Tf is None else Tf
    alpha = p["alpha"] if alpha is None else alpha
    iters_factor = p["iters_per_temp_factor"] if iters_factor is None else iters_factor
    n = len(D)
    tour = list(range(n))
    rng.shuffle(tour)
    cost = tour_cost(tour, D)
    if n < 4:
        return tour, cost
    best, best_cost = tour[:], cost
    T = T0
    iters = iters_factor * n
    while T > Tf:
        for _ in range(iters):
            i = rng.randrange(0, n - 1)
            j = rng.randrange(i + 2, n + 1) if i + 2 <= n else None
            if j is None or j >= n or (i == 0 and j == n - 1):
                continue
            dl = two_opt_delta(tour, D, i, j)
            if dl < 0 or rng.random() < math.exp(-dl / T):
                tour[i + 1:j + 1] = reversed(tour[i + 1:j + 1])
                cost += dl
                if cost < best_cost - 1e-12:
                    best, best_cost = tour[:], cost
        T *= alpha
    return best, tour_cost(best, D)


def mst_tour(D):
    """Prim + recorrido preorden (DFS) del MST = aproximación 2 con atajos."""
    n = len(D)
    in_tree = [False] * n
    key = [math.inf] * n
    parent = [-1] * n
    key[0] = 0.0
    children = [[] for _ in range(n)]
    for _ in range(n):
        u = min((v for v in range(n) if not in_tree[v]), key=lambda v: key[v])
        in_tree[u] = True
        if parent[u] >= 0:
            children[parent[u]].append(u)
        for v in range(n):
            if not in_tree[v] and D[u][v] < key[v]:
                key[v], parent[v] = D[u][v], u
    order, stack = [], [0]
    while stack:
        u = stack.pop()
        order.append(u)
        stack.extend(reversed(children[u]))
    return order


def mst_2opt(D):
    tour = two_opt_local_search(mst_tour(D), D)
    return tour, tour_cost(tour, D)
