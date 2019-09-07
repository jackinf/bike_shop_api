# Backend for Bike Shop app

## Description

React-Native Bike Shop repo - https://github.com/jackinf/BikeShop

## Getting started

### Prepare Firebase app

1. Create a Firebase application. 
2. Download a service account file.
3. Specify service account path
    ```
    GOOGLE_APPLICATION_CREDENTIALS=path/to/service_account.json
    ```
   
### Prepare Python environment

Make sure that Python 3.3+ and PIP 18+ are installed

Restore dependencies:
```
pip install -r requirements.txt
```

Start the app:
```
python server.py
```

Alternatively, it's easier to use `nodemon` for development
```
nodemon server.py
```

## Routes

* `/bikes/search`
