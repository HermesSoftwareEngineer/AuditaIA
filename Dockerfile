FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    gcc \
    libffi-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./src ./src

# Opcional: remover build.sh daqui, rodar migrations no Start Command
# COPY ./build.sh .
# RUN bash ./build.sh

EXPOSE 5000

# Gunicorn direto, sem FLASK_APP redundante
CMD ["gunicorn", "--chdir", "src", "app:create_app()", "--bind", "0.0.0.0:5000"]
