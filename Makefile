

.PHONY: test install dev prod

test:
	python3 -m pytest test/

install:
	pip3 install -r requirements.txt --user

dev:
	uvicorn api:app --host 0.0.0.0 --port 8000 --reload

prod:
	uvicorn api:app --host 0.0.0.0 --port 8000 --workers 4