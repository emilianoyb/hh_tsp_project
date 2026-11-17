{
 "class_balance": {
  "2opt_hill_climbing": [
   241,
   48.2
  ],
  "sa_2opt": [
   176,
   35.2
  ],
  "mst_2opt": [
   83,
   16.6
  ]
 },
 "baseline_acc_test": 0.5234899328859061,
 "models": {
  "DecisionTree": {
   "best_params": {
    "max_depth": 2,
    "min_samples_leaf": 1
   },
   "cv_acc": 0.7094164989939639,
   "test_acc": 0.7114093959731543,
   "regret_abs": 0.04633001616609935,
   "regret_rel_pct": 1.0845319789859997,
   "optimal_picks": 111
  },
  "KNN": {
   "best_params": {
    "n_neighbors": 7,
    "weights": "uniform"
   },
   "cv_acc": 0.703661971830986,
   "test_acc": 0.6912751677852349,
   "regret_abs": 0.046777641537611714,
   "regret_rel_pct": 1.0002930934884815,
   "optimal_picks": 117
  },
  "RandomForest": {
   "best_params": {
    "max_depth": 5,
    "min_samples_leaf": 1
   },
   "cv_acc": 0.7150100603621731,
   "test_acc": 0.697986577181208,
   "regret_abs": 0.036558836189145225,
   "regret_rel_pct": 0.80846196622345,
   "optimal_picks": 119
  }
 },
 "test_acc": 0.7114093959731543,
 "confusion": [
  [
   72,
   6,
   0
  ],
  [
   16,
   34,
   0
  ],
  [
   10,
   11,
   0
  ]
 ],
 "regret_abs_mean": 0.04633001616609935,
 "regret_rel_mean_pct": 1.0845319789859997,
 "pred_counts": {
  "2opt_hill_climbing": 98,
  "sa_2opt": 51,
  "mst_2opt": 0
 },
 "importance_perm": {
  "n": 0.1533,
  "mean_pairwise_dist": 0.109,
  "std_coords": 0.0,
  "mean_centroid_dist": 0.0,
  "mean_nn_dist": 0.0,
  "dist_uniform": 0.0,
  "dist_clustered": 0.0,
  "dist_border": 0.0
 },
 "importance_tree": {
  "n": 0.6634,
  "mean_pairwise_dist": 0.3366,
  "std_coords": 0.0,
  "mean_centroid_dist": 0.0,
  "mean_nn_dist": 0.0,
  "dist_uniform": 0.0,
  "dist_clustered": 0.0,
  "dist_border": 0.0
 },
 "by_distribution": {
  "border": {
   "2opt_hill_climbing": 126,
   "sa_2opt": 19,
   "mst_2opt": 21
  },
  "clustered": {
   "2opt_hill_climbing": 54,
   "sa_2opt": 85,
   "mst_2opt": 28
  },
  "uniform": {
   "2opt_hill_climbing": 61,
   "sa_2opt": 72,
   "mst_2opt": 34
  }
 },
 "by_n": {
  "5": {
   "2opt_hill_climbing": 57,
   "sa_2opt": 0,
   "mst_2opt": 0
  },
  "10": {
   "2opt_hill_climbing": 51,
   "sa_2opt": 2,
   "mst_2opt": 4
  },
  "15": {
   "2opt_hill_climbing": 40,
   "sa_2opt": 10,
   "mst_2opt": 7
  },
  "20": {
   "2opt_hill_climbing": 27,
   "sa_2opt": 14,
   "mst_2opt": 16
  },
  "30": {
   "2opt_hill_climbing": 22,
   "sa_2opt": 23,
   "mst_2opt": 11
  },
  "40": {
   "2opt_hill_climbing": 20,
   "sa_2opt": 24,
   "mst_2opt": 10
  },
  "60": {
   "2opt_hill_climbing": 12,
   "sa_2opt": 34,
   "mst_2opt": 8
  },
  "80": {
   "2opt_hill_climbing": 6,
   "sa_2opt": 34,
   "mst_2opt": 14
  },
  "100": {
   "2opt_hill_climbing": 6,
   "sa_2opt": 35,
   "mst_2opt": 13
  }
 },
 "rel_vs_hc_by_n": {
  "5": {
   "sa_vs_hc": 0.0,
   "mst_vs_hc": 0.0
  },
  "10": {
   "sa_vs_hc": -0.32,
   "mst_vs_hc": 0.01
  },
  "15": {
   "sa_vs_hc": -0.96,
   "mst_vs_hc": 0.01
  },
  "20": {
   "sa_vs_hc": -1.28,
   "mst_vs_hc": -0.28
  },
  "30": {
   "sa_vs_hc": -2.16,
   "mst_vs_hc": -1.07
  },
  "40": {
   "sa_vs_hc": -2.2,
   "mst_vs_hc": -0.56
  },
  "60": {
   "sa_vs_hc": -4.97,
   "mst_vs_hc": -1.85
  },
  "80": {
   "sa_vs_hc": -6.47,
   "mst_vs_hc": -4.22
  },
  "100": {
   "sa_vs_hc": -2.07,
   "mst_vs_hc": -2.34
  }
 },
 "rel_vs_hc_by_dist": {
  "border": {
   "sa_vs_hc": -1.33,
   "mst_vs_hc": -1.02
  },
  "clustered": {
   "sa_vs_hc": -2.33,
   "mst_vs_hc": -0.74
  },
  "uniform": {
   "sa_vs_hc": -3.02,
   "mst_vs_hc": -1.59
  }
 },
 "regret_siempre_2opt_hill_climbing": [
  0.12617003650772018,
  2.6769785754773077
 ],
 "regret_siempre_sa_2opt": [
  0.014217722415956608,
  0.27499133256199243
 ],
 "regret_siempre_mst_2opt": [
  0.07228551459181874,
  1.6895301167373622
 ]
}
