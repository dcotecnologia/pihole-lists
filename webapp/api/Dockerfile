FROM python:3.14-slim
ENV PIP_ROOT_USER_ACTION=ignore

RUN pip install -q --upgrade pip uv

WORKDIR /app
ADD ./pyproject.toml ./uv.lock ./
RUN uv sync --frozen --no-install-project --no-dev

ADD ./app ./app

EXPOSE 8000
CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
