FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./src ./src
COPY ./build.sh .
RUN bash ./build.sh

EXPOSE 5000

CMD ["gunicorn", "--chdir", "src", "app:create_app()", "--bind", "0.0.0.0:5000"]
