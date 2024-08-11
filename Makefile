SHELL=/bin/bash
CONTAINER_NAME=mawinter-fe

.PHONY: build

build:
	docker build -t $(CONTAINER_NAME) -f build/Dockerfile .
