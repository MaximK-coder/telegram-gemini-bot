# Используем официальный образ Python
FROM python:3.11-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем только файлы зависимостей сначала
# Это позволяет кэшировать слои Docker при установке зависимостей
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем сам бот и конфигурацию
COPY tg-bot_ai_gemimi.py .
COPY .env .

# Запускаем бота
CMD ["python", "tg-bot_ai_gemimi.py"]