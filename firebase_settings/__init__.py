import firebase_admin


def init():
    """Documentation about initialization of the Firebase application - https://firebase.google.com/docs/admin/setup"""

    # set GOOGLE_APPLICATION_CREDENTIALS with a path to service account
    firebase_admin.initialize_app(options={"databaseURL": "https://bikeshop-123f1.firebaseio.com"})
