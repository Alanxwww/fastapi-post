# ---- builder ----
FROM python:3.12-slim-bookworm AS builder
ENV PIP_NO_CACHE_DIR=1 PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential gcc python3-dev libffi-dev libssl-dev libpq-dev \
    libxml2-dev libxslt1-dev zlib1g-dev \
 && rm -rf /var/lib/apt/lists/*
WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip setuptools wheel \
 && pip wheel --no-cache-dir --prefer-binary -r requirements.txt -w /wheels

# ---- runtime ----
FROM python:3.12-slim-bookworm
ENV PIP_NO_CACHE_DIR=1 PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /usr/src/app

# 只拷贝打好的 wheels，避免把编译工具带进来
COPY --from=builder /wheels /wheels
RUN pip install --no-cache-dir --no-compile /wheels/*.whl \
 && rm -rf /wheels

# 再拷贝业务代码（已用 .dockerignore 过滤无关内容）
COPY . .

EXPOSE 8000
CMD ["uvicorn","app.main:app","--host","0.0.0.0","--port","8000"]
