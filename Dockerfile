# ---------- React Build ----------
FROM node:22-alpine AS frontend-build

WORKDIR /frontend

COPY frontend-spa/package*.json ./
RUN npm install

COPY frontend-spa/ .

RUN npm run build


# ---------- Django ----------
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

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

COPY --from=frontend-build /frontend/build /usr/share/nginx/html

EXPOSE 80

RUN chmod +x /app/start.sh

CMD ["/app/start.sh"]