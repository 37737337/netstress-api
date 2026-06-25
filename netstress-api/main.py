from fastapi import FastAPI, HTTPException
import subprocess
import re

app = FastAPI(
    title="NetStress API",
    description="REST API для автоматизированного нагрузочного тестирования веб-серверов.",
    version="1.0.0"
)

@app.post("/api/v1/benchmark")
async def run_benchmark(target_url: str, duration: int = 10):
    """
    Запускает утилиту wrk для проверки пропускной способности сервера.
    """
    if not target_url.startswith("http"):
        raise HTTPException(status_code=400, detail="URL должен начинаться с http или https")

    try:
        # Вызываем системную утилиту wrk (2 потока, 100 соединений)
        process = subprocess.run(
            ["wrk", "-t2", "-c100", f"-d{duration}s", target_url],
            capture_output=True,
            text=True,
            timeout=duration + 5
        )
        
        output = process.stdout
        
        # Парсим результаты с помощью регулярных выражений
        rps_match = re.search(r"Requests/sec:\s+([\d.]+)", output)
        latency_match = re.search(r"Latency\s+([\d.]+\w+)", output)
        
        if rps_match:
            return {
                "status": "success",
                "target": target_url,
                "duration_seconds": duration,
                "metrics": {
                    "requests_per_second": float(rps_match.group(1)),
                    "avg_latency": latency_match.group(1) if latency_match else "N/A"
                },
                "raw_output": output
            }
        else:
            return {"status": "error", "detail": "Не удалось получить метрики. Проверьте доступность цели."}

    except subprocess.TimeoutExpired:
        raise HTTPException(status_code=504, detail="Таймаут тестирования (сервер не ответил вовремя)")
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Утилита wrk не установлена в системе")