from typing import List
from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import json
from app.models import multivariate1, multivariate2, multivariate3

app = FastAPI()

@app.get("/")
def doc():
    return {
        "message": "Welcome to the anomaly detector service, based on the talk Implementing Multivariate Anomaly Detection in Python!",
        "documentation": "If you want to see the OpenAPI specification, navigate to the /redoc/ path on this server."
    }

class Multivariate_Input(BaseModel):
    key: str
    vals: list = []
    
@app.post("/detect/multivariate/1")
def post_multivariate1(
    input_data: List[Multivariate_Input],
    sensitivity_score: float = 50,
    max_fraction_anomalies: float = 1.0,
    n_neighbors: int = 10,
    debug: bool = False
):
    df = pd.DataFrame(i.__dict__ for i in input_data)
    (df, weights, details) = multivariate1.detect_multivariate_statistical(df, sensitivity_score, max_fraction_anomalies, n_neighbors)
    
    results = { "anomalies": json.loads(df.to_json(orient='records')) }
    
    if (debug):
        results.update({ "debug_weights": weights })
        results.update({ "debug_details": details })
    return results

@app.post("/detect/multivariate/2")
def post_multivariate2(
    input_data: List[Multivariate_Input],
    sensitivity_score: float = 50,
    max_fraction_anomalies: float = 1.0,
    n_neighbors: int = 10,
    debug: bool = False
):
    df = pd.DataFrame(i.__dict__ for i in input_data)
    
    (df, weights, details) = multivariate2.detect_multivariate_statistical(df, sensitivity_score, max_fraction_anomalies, n_neighbors)
    
    results = { "anomalies": json.loads(df.to_json(orient='records')) }
    
    if (debug):
        results.update({ "debug_weights": weights })
        results.update({ "debug_details": details })
    return results

@app.post("/detect/multivariate/3")
def post_multivariate3(
    input_data: List[Multivariate_Input],
    sensitivity_score: float = 50,
    max_fraction_anomalies: float = 1.0,
    n_neighbors: int = 10,
    debug: bool = False
):
    df = pd.DataFrame(i.__dict__ for i in input_data)
    
    (df, weights, details) = multivariate3.detect_multivariate_statistical(df, sensitivity_score, max_fraction_anomalies, n_neighbors)
    
    results = { "anomalies": json.loads(df.to_json(orient='records')) }
    
    if (debug):
        results.update({ "debug_weights": weights })
        results.update({ "debug_details": details })
    return results
