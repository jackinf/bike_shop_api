import json
import os

import firebase_admin
from firebase_admin import credentials

PRIVATE_KEY_VALUE = "PRIVATE_KEY_VALUE"


def init():
    """Documentation about initialization of the Firebase application - https://firebase.google.com/docs/admin/setup"""

    f = open("service-account.json", "w+")
    output = json.dumps({
        "type": "service_account",
        "project_id": "bikeshop-123f1",
        "private_key_id": "ebd0a338499c8e2b276e1e246f76cd22cad02ac3",
        "private_key": PRIVATE_KEY_VALUE,
        "client_email": "firebase-adminsdk-2ly68@bikeshop-123f1.iam.gserviceaccount.com",
        "client_id": "104574911429780415218",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-2ly68%40bikeshop-123f1.iam.gserviceaccount.com"
    })
    output = output.replace(PRIVATE_KEY_VALUE, os.getenv('BIKE_SHOP_SERVICE_ACCOUNT_PRIVATE_KEY'))
    f.write(output)
    f.close()

    if os.getenv('GOOGLE_APPLICATION_CREDENTIALS') is None:
        firebase_admin.initialize_app(
            options={"databaseURL": os.getenv('BIKE_SHOP_DATABASE_URL')},  # "https://bikeshop-123f1.firebaseio.com"
            credential=credentials.Certificate('service-account.json')
        )
    else:
        firebase_admin.initialize_app(options={"databaseURL": os.getenv('BIKE_SHOP_DATABASE_URL')})
