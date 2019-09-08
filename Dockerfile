FROM python:3.7
COPY requirements.txt /
RUN pip install -r requirements.txt
COPY . /
ENV GOOGLE_APPLICATION_CREDENTIALS="./__sensitive__/bikeshop-123f1-firebase-adminsdk-2ly68-ebd0a33849.json"
CMD [ "python", "-u", "server.py" ]