# ---------- React Build ----------
FROM node:22-alpine AS frontend-build

WORKDIR /frontend

COPY frontend-spa/package*.json ./
RUN npm install

COPY frontend-spa/ .

RUN npm run build


# ---------- Django + Gunicorn + Nginx ----------
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    pkg-config \
    default-libmysqlclient-dev \
    libcairo2-dev \
    libffi-dev \
    libjpeg-dev \
    zlib1g-dev \
    libxml2-dev \
    libxslt1-dev \
    libfreetype6-dev \
    nginx \
    && rm -rf /var/lib/apt/lists/*

# Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend
COPY . .

# Copy React build
COPY --from=frontend-build /frontend/build /usr/share/nginx/html

# Copy nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Make startup script executable
RUN chmod +x /app/start.sh

EXPOSE 80

CMD ["/app/start.sh"]