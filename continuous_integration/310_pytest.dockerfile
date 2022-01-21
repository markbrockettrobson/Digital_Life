FROM python:3.10

RUN apt update
RUN apt install -y libspatialindex-dev

RUN mkdir /usr/project
WORKDIR /usr/project

COPY requirements.txt ./
COPY requirements_test.txt ./
RUN python -m pip install --no-cache-dir -r requirements_test.txt

COPY pyproject.toml ./
COPY digital_life ./digital_life

RUN python -m pytest --black --isort --pylint --mypy --cov .

#docker build -t 310_pytest -f continuous_integration/310_pytest.dockerfile .