FROM ubuntu:20.04

EXPOSE 8000

WORKDIR /api

COPY requirements.txt /api

RUN apt update && apt install python3-pip libmysqlclient-dev -y && pip install -r requirements.txt 
RUN pip install opencv-python-headless

ENV PYTHONPATH=/api

ADD . /api

CMD ["python3", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]