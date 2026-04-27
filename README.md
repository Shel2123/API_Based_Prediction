# API_Based_Prediction

A project where a scikit-learn model is wrapped in a three-tier service architecture:
**Python frontend → Go (Gin) gateway → FastAPI with the model**.
The whole stack comes up with a single `docker compose` command.

The point of the project isn't the model itself — it's the end-to-end exercise:
splitting responsibilities across services, getting them to talk over HTTP,
and packaging everything so it runs reproducibly anywhere.

## Why three services for one model?

To get hands-on with a pattern that shows up a lot in production: a thin client, a fast gateway in front, and a heavier Python ML backend behind it.
Two practical wins from this layout:
- The gateway can be scaled or have caching/rate limiting added independently of the heavier Python process.
- The ML service is isolated, so the model can be retrained and swapped without touching the rest of the stack.

## The model

**Task.** Binary classification - given a person's profile, predict whether their credit score
qualifies as `High` (label `1`) or not (`Average`/`Low` collapsed to `-1`). Dataset:
[Credit Score Classification Dataset](https://www.kaggle.com/datasets/sujithmandala/credit-score-classification-dataset)
(Kaggle), kept locally in `data/`.

**Algorithm.** `LogisticRegression` from scikit-learn (`max_iter=1000`). A linear model is a
natural choice here: the dataset is small, the feature set is low-dimensional, and a
logistic regression gives me interpretable coefficients and a calibrated `predict_proba` —
which is exactly what I need to report ROC AUC.

**Features and preprocessing.**
- `Education` and `Number of Children` dropped - weak/irrelevant signal for this target.
- Categorical features encoded as `{-1, +1}`: `Gender`, `Marital Status`, `Home Ownership`. With only two categories each, this is equivalent to one-hot but keeps the feature matrix narrower.
- `Income` → `log1p` to compress the right tail, then clipped at the 99th percentile to limit the influence of outliers, then standardized with `StandardScaler`.
- `Age` standardized with `StandardScaler`.


## Running it

### Option 1: Docker Compose (recommended)

```bash
docker compose up --build
```

Brings up all three services at once.

### Option 2: Locally, service by service

```bash
pip install -r requirements.txt

# ML service (FastAPI)
uvicorn python_api.app:app --host 127.0.0.1 --port 8000 --reload

# Gateway (Go + Gin)
go run go_api/main.go

# Frontend
python web/main.py
```
