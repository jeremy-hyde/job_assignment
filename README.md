# Job Assignment

## Installation

### Pyenv + Poetry

Prerequisites
- pyenv
- poetry

### Libs
#### Ubuntu
```shell
sudo apt-get install python3-dev build-essential
```

#### Pyenv Installation  

```shell
curl https://pyenv.run | bash
```

Installation de python 3.12.3
```shell
pyenv install 3.12.3
```

#### Poetry installation

```shell
curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python
```

Poetry Configuration
```shell
poetry config virtualenvs.in-project true
```

#### Project Installation
```shell
poetry install
```

#### Activate virtual env
```shell
source .venv/bin/activate
```

or 

```shell
poetry shell
```

## Run
After activation the virtual env
```shell
python main.py "10 10                                                                                                                                     .venv  (master|●💩?) 13:28
                1 3 N
                FFRFFFRRLFRFL"
```

## Dev Commands
Run tests
```shell
python -m pytest -x -v --cov=src --cov-config .coveragerc --cov-report html --cov-report term-missing --junit-xml=xunit-reports/xunit-result-pytest.xml tests
```

Run formatting
```shell
ruff check --select I --fix src tests && ruff format src tests
```

Run lint check
```shell
ruff check src tests
```
