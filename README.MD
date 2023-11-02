To run the whole project:
```sh
./deploy.sh
```


To create a virtual env:
```sh
python -m venv .venv
```

To activate the virtual environment once it is installed run:
```sh
source .venv/bin/activate
```

To activate uvicorn:
```sh
uvicorn main:app --reload
```