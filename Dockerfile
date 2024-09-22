FROM python:3.12 AS base
ARG ENVIRONMENT=development

ENV IN_CONTAINER=1 \
  PATH=$PATH:/src \
  POETRY_VIRTUALENVS_CREATE=false \
  PIP_ROOT_USER_ACTION=ignore \
  PIP_PKGS_PATH=/usr/local/lib/python3.12/site-packages

RUN pip install -q --upgrade pip poetry ipython
RUN poetry config installer.max-workers 10

FROM base AS build-stage
WORKDIR /src
ADD ./poetry.lock ./pyproject.toml ./

RUN poetry install $(test "$ENVIRONMENT" != "development" && echo "--no-dev") --no-interaction --no-ansi --no-root

FROM base AS runner
WORKDIR /src

COPY --from=build-stage $PIP_PKGS_PATH $PIP_PKGS_PATH

ADD ./src/ ./
ADD ./lists/ ./lists/
ADD ./.version ./

CMD ["python", "-m", "cleanup"]
