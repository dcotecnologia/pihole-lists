FROM python:3.12 as base
ARG ENVIRONMENT development
ENV IN_CONTAINER 1
ENV PATH $PATH:/src
ENV POETRY_VIRTUALENVS_CREATE="false"
ENV PIP_ROOT_USER_ACTION="ignore"
ENV PIP_PKGS_PATH=/usr/local/lib/python3.12/site-packages

RUN pip install -q --upgrade pip
RUN pip install poetry ipython
RUN poetry config installer.max-workers 10

FROM base as build-stage
WORKDIR /src
ADD ./src/poetry.lock ./src/pyproject.toml ./
RUN poetry install $(test "$ENVIRONMENT" != "development" && echo "--no-dev") --no-interaction --no-ansi --no-root

FROM base as runner
WORKDIR /src
COPY --from=build-stage $PIP_PKGS_PATH $PIP_PKGS_PATH
ADD ./src/. .version ./

CMD ["python", "-m", "main"]