BRANCH := $(shell git rev-parse --abbrev-ref HEAD)

default:
	docker-compose run build

cleanup:
	docker-compose run cleanup