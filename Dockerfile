# Використовуємо офіційний базовий образ Python
#task 1
FROM python:3.10-slim

# Встановлюємо робочу директорію
WORKDIR /usr/src/app

# Копіюємо файл залежностей
COPY app/requirements.txt ./

# Встановлюємо залежності
RUN pip install --no-cache-dir -r requirements.txt

# Копіюємо вміст локальної папки 'app/' в робочу директорію контейнера '.'
COPY app/ .

# Відкриваємо порт, який використовує Flask
EXPOSE 5000

# ✅ СКОРИГОВАНО: Команда для запуску застосунку (app.py)
CMD ["python", "app.py"]