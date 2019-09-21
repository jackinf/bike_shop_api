FROM python:3.7
COPY requirements.txt /
RUN pip install -r requirements.txt
COPY . /
ENV BIKE_SHOP_SERVICE_ACCOUNT_PRIVATE_KEY=""
CMD [ "python", "-u", "server.py" ]