SHELL=/bin/bash
container_name=mawinter-front
.PHONY: build

build:
	docker build -t $(container_name):latest -f Dockerfile .
