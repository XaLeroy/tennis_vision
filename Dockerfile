FROM python:3.10.13-slim-bullseye
WORKDIR /prod
# First, pip install dependencies
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
# Then the rest
COPY YoloV3 yolo_v3
COPY WeightsTracknet tracknet
COPY api api
COPY sort.py sort.py
COPY court_detector.py court_detector.py
COPY court_reference.py court_reference.py
COPY detection.py detection.py
#  Let the magic happen
RUN printenv
CMD uvicorn api.fast_api:app --host 0.0.0.0 --port $PORT
