

.PHONY: test install dev prod

test:
	python3 -m pytest test/

install:
	pip3 install -r requirements.txt --user

dev:
	uvicorn api:app --host 0.0.0.0 --port 8000 --reload

prod:
	docker-compose -f build/docker-compose.yml up -d

build:
	docker build --tag nih-backend:latest . -f build/Dockerfile
