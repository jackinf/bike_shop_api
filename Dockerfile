FROM python:3.7-slim
COPY requirements.txt /
RUN pip install -r requirements.txt
COPY . /
ENV BIKE_SHOP_SERVICE_ACCOUNT_PRIVATE_KEY=""
EXPOSE 8082
CMD [ "python", "-u", "server.py" ]