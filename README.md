# Clincial Trial System


### Install env
```
$ pip3 install -r requirements.txt
```

### Launch dev server
```
$ python -m uvicorn api:app --host 0.0.0.0 --port 8000 --reload
```

### Launch api server
```
$ python -m uvicorn api:app --host 0.0.0.0 --port 8000 --workers 4

