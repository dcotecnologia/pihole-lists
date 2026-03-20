FROM python:3.14 AS base
ARG ENVIRONMENT=development

ENV IN_CONTAINER=1 \
  PATH=$PATH:/src \
  UV_PROJECT_ENVIRONMENT=/usr/local \
  PIP_ROOT_USER_ACTION=ignore \
  PIP_PKGS_PATH=/usr/local/lib/python3.14/site-packages

RUN pip install -q --upgrade pip uv ipython

FROM base AS build-stage
WORKDIR /src
ADD ./uv.lock ./pyproject.toml ./

RUN uv sync $(test "$ENVIRONMENT" != "development" && echo "--no-dev") --frozen --no-install-project

FROM base AS runner
WORKDIR /src

COPY --from=build-stage $PIP_PKGS_PATH $PIP_PKGS_PATH

ADD ./src/ ./
ADD ./lists/ ./lists/

CMD ["python", "-m", "cleanup"]
