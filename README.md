# Extraction

Extraction is REST API for predicting prospect's conversion probability and potential MMR.


## Getting Started

Environment set up depends on [brew](https://brew.sh/). Python and dependencies install steps are followings:

1. Install Python `brew install python@3.12`
2. Install [Poetry](https://python-poetry.org/) for dependency management `pip3 install poetry`
3. Create virtual environment `poetry env use python3.12`
4. Activate the virtual environment `poetry shell`
5. Install dependencies `poetry install`

Steps for running Extraction locally:
1. Start the server `./scripts/start.sh`
2. Navigate to [localhost:8008/docs](http://localhost:8008/docs)


## Running Tests

Testing first requires [environment setup](#getting-started). Once the environment set up, tests
can be run using:

```bash
python -m pytest tests
```

## Linting

[Flake8](https://flake8.pycqa.org/en/latest/) is used for linting and can be run using:

```bash
flake8
```

## Configuration

Configuration options such as model version are defined in `.env` file.
