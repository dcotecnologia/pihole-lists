BRANCH := $(shell git rev-parse --abbrev-ref HEAD)
DOCKER_COMPOSE_CMD := docker-compose run

.PHONY: default cleanup

default:
	$(DOCKER_COMPOSE_CMD) build

cleanup:
	$(DOCKER_COMPOSE_CMD) cleanup
