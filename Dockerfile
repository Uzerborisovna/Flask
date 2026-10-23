# Берем легкий Python
FROM python:3.11-slim

# Создаем рабочую папку
WORKDIR /app

# Копируем файл с зависимостями (создадим его следующим шагом)
COPY requirements.txt .

# Устанавливаем Flask и Gunicorn
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь наш код
COPY . .

# Открываем порт
EXPOSE 5000

# Запускаем через Gunicorn (как учили на лекции)
CMD ["gunicorn", "-b", "0.0.0.0:5000", "--capture-output", "app:app"]