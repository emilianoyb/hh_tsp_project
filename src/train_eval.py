"""Parte 2: clasificador de la hiper-heurística, evaluación y análisis."""
import os, json
import numpy as np, pandas as pd
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import GridSearchCV, StratifiedKFold
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.inspection import permutation_importance

ROOT = os.path.join(os.path.dirname(__file__), "..")
DATA, RES = os.path.join(ROOT, "data"), os.path.join(ROOT, "results")
SEED = 42
ALGS = ["2opt_hill_climbing", "sa_2opt", "mst_2opt"]
COST = {"2opt_hill_climbing": "cost_2opt_hill_climbing", "sa_2opt": "cost_sa_2opt", "mst_2opt": "cost_mst_2opt"}
NUM = ["n", "mean_pairwise_dist", "std_coords", "mean_centroid_dist", "mean_nn_dist"]

tr = pd.read_csv(f"{DATA}/train_labeled.csv"); te = pd.read_csv(f"{DATA}/test_labeled.csv")
allf = pd.concat([tr, te], ignore_index=True)

def X_of(df):
    X = df[NUM].copy()
    for d in ["uniform", "clustered", "border"]:
        X[f"dist_{d}"] = (df["distribution"] == d).astype(int)
    return X
Xtr, Xte, ytr, yte = X_of(tr), X_of(te), tr.best_algorithm, te.best_algorithm
out = {}

# ---- balance de clases (500 instancias) ----
bal = allf.best_algorithm.value_counts().reindex(ALGS)
out["class_balance"] = {a: [int(bal[a]), round(100 * bal[a] / len(allf), 1)] for a in ALGS}
out["class_balance_train"] = tr.best_algorithm.value_counts().reindex(ALGS).fillna(0).astype(int).to_dict()
out["class_balance_test"] = yte.value_counts().reindex(ALGS).fillna(0).astype(int).to_dict()
majority = bal.idxmax()
out["majority"] = majority
out["baseline_acc_test"] = float((yte == majority).mean())

# ---- selección de modelo por CV estratificada en train ----
cv = StratifiedKFold(5, shuffle=True, random_state=SEED)
grids = {
    "DecisionTree": (DecisionTreeClassifier(random_state=SEED, class_weight=None),
                     {"max_depth": [2, 3, 4, 5, 6, 8, None], "min_samples_leaf": [1, 3, 5, 10]}),
    "KNN": (make_pipeline(StandardScaler(), KNeighborsClassifier()),
            {"kneighborsclassifier__n_neighbors": [1, 3, 5, 7, 9, 15, 25], "kneighborsclassifier__weights": ["uniform", "distance"]}),
    "RandomForest": (RandomForestClassifier(random_state=SEED, n_estimators=300),
                     {"max_depth": [3, 5, None], "min_samples_leaf": [1, 3, 5]}),
}
models, res = {}, {}
for name, (est, g) in grids.items():
    gs = GridSearchCV(est, g, cv=cv, scoring="accuracy").fit(Xtr, ytr)
    models[name] = gs.best_estimator_
    pred = gs.predict(Xte)
    res[name] = dict(best_params={k.split("__")[-1]: v for k, v in gs.best_params_.items()}, cv_acc=float(gs.best_score_),
                     test_acc=float(accuracy_score(yte, pred)))
out["models"] = res
chosen = "DecisionTree"   # modelo principal (sugerido); los demás se reportan como comparación

def regret(df, pred):
    chosen_cost = np.array([df.loc[i, COST[p]] for i, p in zip(df.index, pred)])
    best = df[list(COST.values())].min(axis=1).values
    return chosen_cost - best, (chosen_cost - best) / best * 100

for name, m in models.items():
    pred = m.predict(Xte)
    ab, rel = regret(te, pred)
    res[name].update(regret_abs=float(ab.mean()), regret_rel_pct=float(rel.mean()),
                     optimal_picks=int((ab < 1e-9).sum()))
# referencias de regret
for nm, fixed in [("siempre_" + a, [a] * len(te)) for a in ALGS]:
    ab, rel = regret(te, fixed); out[f"regret_{nm}"] = [float(ab.mean()), float(rel.mean())]

m = models[chosen]; pred = m.predict(Xte)
ab, rel = regret(te, pred)
out["chosen"] = chosen
out["test_acc"] = float(accuracy_score(yte, pred))
out["confusion"] = confusion_matrix(yte, pred, labels=ALGS).tolist()
out["report"] = classification_report(yte, pred, labels=ALGS, output_dict=True, zero_division=0)
out["regret_abs_mean"], out["regret_rel_mean_pct"] = float(ab.mean()), float(rel.mean())
out["regret_abs_median"], out["regret_abs_max"] = float(np.median(ab)), float(ab.max())
out["pred_counts"] = pd.Series(pred).value_counts().reindex(ALGS).fillna(0).astype(int).to_dict()
out["optimal_picks"] = int((ab < 1e-9).sum())
# regret condicionado a la clase real
te2 = te.assign(pred=pred, regret=ab, regret_rel=rel)
out["regret_by_true_class"] = te2.groupby("best_algorithm").regret.mean().to_dict()
# pérdida media de cada selector fijo sobre el costo óptimo y oráculo
out["mean_best_cost"] = float(te[list(COST.values())].min(axis=1).mean())
te2.to_csv(f"{RES}/test_predictions.csv", index=False)

# ---- empates y sensibilidad ----
cc = list(COST.values())
def ties(df): 
    c = df[cc].round(9); return (c.eq(c.min(axis=1), axis=0)).sum(axis=1)
nt_all, nt_te = ties(allf), ties(te)
out["n_ties_all"], out["n_ties_test"] = int((nt_all > 1).sum()), int((nt_te > 1).sum())
out["ties_by_n"] = allf[nt_all > 1].groupby("n").size().to_dict()
out["balance_strict_winners"] = allf[nt_all == 1].best_algorithm.value_counts().reindex(ALGS).fillna(0).astype(int).to_dict()
mask = (nt_te == 1).values
out["test_acc_no_ties"] = float(accuracy_score(yte[mask], pred[mask])); out["test_n_no_ties"] = int(mask.sum())
out["baseline_acc_no_ties"] = float((yte[mask] == majority).mean())
out["test_balance_no_ties"] = yte[mask].value_counts().reindex(ALGS).fillna(0).astype(int).to_dict()

# ---- importancia de características ----
imp_tree = pd.Series(m.feature_importances_, index=Xtr.columns)
pi = permutation_importance(m, Xte, yte, n_repeats=50, random_state=SEED)
imp_perm = pd.Series(pi.importances_mean, index=Xtr.columns)
out["importance_tree"] = imp_tree.round(4).to_dict(); out["importance_perm"] = imp_perm.round(4).to_dict()

# ---- patrones por distribución y tamaño (500 instancias) ----
for key, col in [("by_distribution", "distribution"), ("by_n", "n")]:
    ct = pd.crosstab(allf[col], allf.best_algorithm).reindex(columns=ALGS, fill_value=0)
    out[key] = ct.to_dict("index")
ct = pd.crosstab([allf.distribution, allf.n], allf.best_algorithm).reindex(columns=ALGS, fill_value=0)
ct.to_csv(f"{RES}/winners_by_dist_n.csv")
# mejora relativa media de SA y MST sobre HC
allf["sa_vs_hc"] = (allf.cost_sa_2opt / allf.cost_2opt_hill_climbing - 1) * 100
allf["mst_vs_hc"] = (allf.cost_mst_2opt / allf.cost_2opt_hill_climbing - 1) * 100
out["rel_vs_hc_by_n"] = allf.groupby("n")[["sa_vs_hc", "mst_vs_hc"]].mean().round(2).to_dict("index")
out["rel_vs_hc_median_by_dist"] = allf.groupby("distribution")[["sa_vs_hc", "mst_vs_hc"]].median().round(2).to_dict("index")
out["rel_vs_hc_by_dist"] = allf.groupby("distribution")[["sa_vs_hc", "mst_vs_hc"]].mean().round(2).to_dict("index")

# ---- figuras ----
from sklearn.tree import plot_tree
fig, ax = plt.subplots(figsize=(14, 7))
plot_tree(m, feature_names=list(Xtr.columns), class_names=list(m.classes_), filled=True, ax=ax, fontsize=7, max_depth=4)
fig.savefig(f"{RES}/tree.png", dpi=150, bbox_inches="tight"); plt.close(fig)

fig, ax = plt.subplots(figsize=(5, 4))
cm = np.array(out["confusion"]); ax.imshow(cm, cmap="Blues")
ax.set_xticks(range(3)); ax.set_yticks(range(3)); ax.set_xticklabels(["HC", "SA", "MST"]); ax.set_yticklabels(["HC", "SA", "MST"])
ax.set_xlabel("Predicho"); ax.set_ylabel("Real")
for i in range(3):
    for j in range(3): ax.text(j, i, cm[i, j], ha="center", va="center", color="white" if cm[i, j] > cm.max() / 2 else "black")
fig.savefig(f"{RES}/confusion.png", dpi=150, bbox_inches="tight"); plt.close(fig)

fig, ax = plt.subplots(figsize=(6, 3.5))
imp_perm.sort_values().plot.barh(ax=ax, color="#4472C4"); ax.set_xlabel("Importancia por permutación (caída de accuracy, test)")
fig.savefig(f"{RES}/importance.png", dpi=150, bbox_inches="tight"); plt.close(fig)

fig, axs = plt.subplots(1, 2, figsize=(10, 3.8))
for ax, col, order in [(axs[0], "distribution", ["uniform", "clustered", "border"]), (axs[1], "n", sorted(allf.n.unique()))]:
    ct = pd.crosstab(allf[col], allf.best_algorithm).reindex(index=order, columns=ALGS, fill_value=0)
    (ct.div(ct.sum(axis=1), axis=0) * 100).plot.bar(stacked=True, ax=ax, color=["#4472C4", "#ED7D31", "#70AD47"], legend=False, rot=0)
    ax.set_ylabel("% instancias ganadas"); ax.set_xlabel(col)
axs[1].legend(["2-opt HC", "SA+2-opt", "MST+2-opt"], fontsize=7, loc="upper center", bbox_to_anchor=(0.5, 1.18), ncol=3, frameon=False)
fig.tight_layout(); fig.savefig(f"{RES}/winners.png", dpi=150); plt.close(fig)

json.dump(out, open(f"{RES}/metrics.json", "w"), indent=1, default=str)
print(json.dumps({k: out[k] for k in ["class_balance", "baseline_acc_test", "models", "test_acc", "confusion", "regret_abs_mean", "regret_rel_mean_pct", "pred_counts", "importance_perm", "importance_tree", "by_distribution", "by_n", "rel_vs_hc_by_n", "rel_vs_hc_by_dist"] + [k for k in out if k.startswith("regret_siempre")]}, indent=1, default=str))
