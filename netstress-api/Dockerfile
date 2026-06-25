FROM python:3.11-slim

# Обновляем систему и устанавливаем системную утилиту wrk
RUN apt-get update && \
    apt-get install -y wrk && \
    rm -rf /var/lib/apt/lists/*

# Создаем рабочую директорию
WORKDIR /app

# Копируем и устанавливаем зависимости Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем код приложения
COPY . .

# Открываем порт для FastAPI
EXPOSE 8000

# Запускаем uvicorn сервер
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]