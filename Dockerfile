FROM python:3.11-slim

WORKDIR /app

# Instala dependências do sistema necessárias para vários pacotes Python
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
COPY ./build.sh .
RUN bash ./build.sh

EXPOSE 5000

CMD ["gunicorn", "--chdir", "src", "app:create_app()", "--bind", "0.0.0.0:5000"]
