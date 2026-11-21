# Hiper-heurística de selección para TSP

Dado una instancia de TSP, un clasificador predice cuál de tres algoritmos obtiene el menor costo:
2-opt hill climbing, SA + 2-opt o MST + 2-opt.

## Cómo correrlo

```bash
pip install -r requirements.txt          # dependencias con versiones fijas
python src/generate_labels.py            # Parte 1: corre los 3 algoritmos y crea data/train_labeled.csv y data/test_labeled.csv
python src/train_eval.py                 # Parte 2: entrena, evalúa y escribe results/
```

Ejecuta los comandos desde la raíz del repositorio. Todo usa semilla fija (42) y tarda ~1 minuto en 2 núcleos
(casi todo en `generate_labels.py`). Opcional: `python src/sa_config_check.py` reproduce la comparación de configuraciones de SA.

## Contenido

- `data/instances/` – coordenadas de las 500 instancias; `data/train.csv` y `data/test.csv` – entradas sin etiquetar.
- `data/train_labeled.csv`, `data/test_labeled.csv` – salida de la Parte 1 (costos de los 3 algoritmos y `best_algorithm`).
- `src/tsp_algorithms.py` – los tres algoritmos (parámetros de SA en `SA_PARAMS`).
- `src/generate_labels.py` – Parte 1. `src/train_eval.py` – Parte 2. `src/sa_config_check.py` – elección de parámetros de SA.
- `results/` – salidas de `train_eval.py`:
  - `metrics.json`: balance de clases, accuracy, matriz de confusión, regret, importancias y patrones por distribución/tamaño.
  - `test_predictions.csv`: predicción y regret por instancia de prueba.
  - `winners_by_dist_n.csv`: ganadores por (distribución, n).
  - `confusion.png`, `importance.png`, `tree.png`, `winners.png`: figuras del reporte.

## Parámetros de etiquetado

- SA: T0 = 0.1, Tf = 1e-4, enfriamiento geométrico α = 0.98, 20·n iteraciones por temperatura, vecindario 2-opt aleatorio, inicio aleatorio.
- HC: inicio aleatorio, mejor mejora 2-opt hasta óptimo local. MST + 2-opt: Prim, preorden, 2-opt.
- Empates (costos iguales tras redondear a 9 decimales): gana el algoritmo más barato computacionalmente (HC < MST + 2-opt < SA).
