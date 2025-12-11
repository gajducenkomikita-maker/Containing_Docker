# task 2
import os

from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/info")
def info():
    # Отримуємо ім'я хосту контейнера, щоб підтвердити, що запит пройшов через мережу Docker
    hostname = os.uname().nodename
    return jsonify(
        {
            "service": "Service A",
            "status": "Running",
            "message": "Hello from Microservice A!",
            "hostname": hostname,
        }
    )


@app.route("/")
def health_check():
    return "Service A is alive"


if __name__ == "__main__":
    # Flask повинен слухати на всіх інтерфейсах (0.0.0.0) на внутрішньому порту 5000
    app.run(host="0.0.0.0", port=5000)
