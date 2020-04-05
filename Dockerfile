FROM python:3.6.8
MAINTAINER "HWNT DEV TEAM"
RUN mkdir -p /backend
COPY . /backend
RUN pip install -r /backend/requirements.txt
WORKDIR /backend
ENTRYPOINT [ "python" ]
CMD [ "run.py" ]
