# Clincial Trial System


### Install env
```
$ pip3 install -r requirements.txt
```

### Launch dev server
```
$ python -m uvicorn api:app --host 0.0.0.0 --port 8000 --reload
```

### Launch api server with multi workers
```
$ python -m uvicorn api:app --host 0.0.0.0 --port 8000 --workers 4
```
### Remember to change search-by-rank.html ip or dns
> Search this: 
>> // You should change this to your server ip or to dns

### Pull this project to your branch
```
$ git fetch --all
$ git merge origin/main
$ git push
```
### Remove current change
```
$ git reset --hard
```