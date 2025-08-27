FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    git \
    postgresql-client \
    curl \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip first
RUN python -m pip install --upgrade pip

# Copy and install requirements
COPY requirements.txt .
RUN pip install --no-cache-dir --no-deps Flask==3.0.0 && \
    pip install --no-cache-dir --no-deps Werkzeug==3.0.1 && \
    pip install --no-cache-dir --no-deps Flask-SQLAlchemy==3.1.1 && \
    pip install --no-cache-dir --no-deps Flask-Migrate==4.0.5 && \
    pip install --no-cache-dir --no-deps Flask-CORS==4.0.0 && \
    pip install --no-cache-dir --no-deps PyJWT==2.8.0 && \
    pip install --no-cache-dir --no-deps python-dotenv==1.0.0 && \
    pip install --no-cache-dir --no-deps psycopg2-binary==2.9.9 && \
    pip install --no-cache-dir --no-deps gunicorn==21.2.0

# Install missing dependencies
RUN pip install --no-cache-dir \
    click \
    itsdangerous \
    Jinja2 \
    MarkupSafe \
    SQLAlchemy \
    typing_extensions \
    alembic \
    Mako

# Copy application code
COPY . .

# Create logs directory
RUN mkdir -p logs

# Create non-root user
RUN useradd --create-home --shell /bin/bash app \
    && chown -R app:app /app
USER app

# Expose port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/v1/auth/health || exit 1

# Start command
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--timeout", "60", "src.app:create_app()"]
