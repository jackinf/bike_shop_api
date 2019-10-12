FROM python:3.7-slim
COPY requirements.txt /
RUN pip install -r requirements.txt
COPY . /
EXPOSE 8082
CMD [ "python", "-u", "server.py" ]