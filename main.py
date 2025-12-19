import time
import random
from fastapi import FastAPI
from prometheus_client import Histogram, generate_latest, CONTENT_TYPE_LATEST
from fastapi.responses import Response

# Определяем гистограмму для задержки запросов
REQUEST_LATENCY = Histogram(
    "request_latency_seconds",
    "Request latency in seconds",
    buckets=[0.1, 0.25, 0.5, 0.75, 1.0, 1.5, 2.0, 3.0, 5.0, 10.0]
)

app = FastAPI()

@app.get("/predict")
@REQUEST_LATENCY.time()
def predict():
    """
    Эмуляция ML-запроса с переменной задержкой.
    Иногда имитируем долгий запрос (>1 сек) для проверки алерта.
    """
    # Случайная задержка от 0.1 до 2.5 секунд
    delay = random.uniform(0.1, 2.5)
    time.sleep(delay)
    return {"prediction": "OK", "latency_sec": round(delay, 2)}

@app.get("/metrics")
def metrics():
    """Эндпоинт для сбора метрик Prometheus"""
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
