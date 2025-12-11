import os
import time
from typing import List, Dict, Any

import psycopg2
from flask import Flask, jsonify

# --- Ініціалізація Flask ---
app = Flask(__name__)

# --- Налаштування бази даних з environment змінних ---
# Використовуємо 'user_db' для уніфікації користувача та бази даних
DB_NAME = os.environ.get("POSTGRES_DB", "user_db")
DB_USER = os.environ.get("POSTGRES_USER", "user_db")
DB_PASSWORD = os.environ.get("POSTGRES_PASSWORD", "password")
DB_HOST = os.environ.get("POSTGRES_HOST", "db")
DB_PORT = os.environ.get("POSTGRES_PORT", "5432")

conn = None


def get_db_connection():
    """Спроба підключення до БД з механізмом повтору."""
    global conn

    if conn and not conn.closed:
        return conn

    max_retries = 10
    retry_delay = 5

    print(f"Спроба підключення до БД: Host={DB_HOST}, DB={DB_NAME}, User={DB_USER}")

    for i in range(max_retries):
        try:
            conn = psycopg2.connect(
                dbname=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD,
                host=DB_HOST,
                port=DB_PORT,
                connect_timeout=5,
            )
            print("База даних успішно підключена!")

            # --- Створення тестової таблиці та даних ---
            with conn.cursor() as cur:
                cur.execute(
                    "CREATE TABLE IF NOT EXISTS users ("
                    "id SERIAL PRIMARY KEY, "
                    "username VARCHAR(100) NOT NULL, "
                    "email VARCHAR(100) NOT NULL);"
                )
                cur.execute("SELECT COUNT(*) FROM users;")
                if cur.fetchone()[0] == 0:
                    cur.execute(
                        "INSERT INTO users (username, email) VALUES "
                        "('Ivan_Docker', 'ivan@example.com'), "
                        "('Olena_Flask', 'olena@example.com');"
                    )
            conn.commit()
            return conn

        except psycopg2.OperationalError as e:
            print(
                f"Спроба {i + 1}/{max_retries}: Помилка підключення до БД ({e}). Очікування {retry_delay}s..."
            )
            time.sleep(retry_delay)

    raise Exception("Не вдалося підключитися до бази даних після кількох спроб.")


@app.route("/users")
def list_users():
    """Ендпоінт, що повертає список користувачів з БД."""
    try:
        connection = get_db_connection()

        with connection.cursor() as cur:
            cur.execute("SELECT id, username, email FROM users;")
            users_data = cur.fetchall()

            users_list: List[Dict[str, Any]] = []
            for user in users_data:
                users_list.append(
                    {"id": user[0], "username": user[1], "email": user[2]}
                )

        return jsonify(users_list)

    except Exception as e:
        return jsonify({"error": "Помилка сервера", "details": str(e)}), 500


@app.route("/")
def home():
    """Простий тестовий ендпоінт."""
    return "Web Service is running. Access /users to see data from PostgreSQL."


if __name__ == "__main__":
    try:
        get_db_connection()
    except Exception as e:
        print(
            f"Критична помилка ініціалізації БД. Сервер запущено, але ендпоінт /users може не працювати: {e}"
        )

    app.run(host="0.0.0.0", port=5000)
