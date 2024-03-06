FROM python:3.10.13-slim-bullseye
WORKDIR /prod
# First, pip install dependencies
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
# Then the rest
COPY . .
CMD uvicorn api.fast_api:app --host 0.0.0.0
#--port ${PORT:-8000}
