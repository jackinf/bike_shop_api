<div align="center">

# Bike Shop API

### Async Python backend for the BikeShop React Native app

[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
![aiohttp](https://img.shields.io/badge/aiohttp-2C5BB4?style=for-the-badge&logo=aiohttp&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)
![Firebase](https://img.shields.io/badge/Firebase-FFCA28?style=for-the-badge&logo=firebase&logoColor=black)
![Stripe](https://img.shields.io/badge/Stripe-635BFF?style=for-the-badge&logo=stripe&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Swagger](https://img.shields.io/badge/Swagger-85EA2D?style=for-the-badge&logo=swagger&logoColor=black)
[![Repo](https://img.shields.io/badge/GitHub-jackinf%2Fbike__shop__api-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/jackinf/bike_shop_api)

</div>

## Overview

Bike Shop API is the backend service for the [BikeShop React Native application](https://github.com/jackinf/BikeShop). It is an asynchronous HTTP API built on `aiohttp`, organized around feature modules for bikes, carts, checkout, payments, and authentication. The service uses Firebase for auth/Firestore, PostgreSQL (via Peewee) for relational data, and Stripe for payment processing, and it exposes a Swagger-documented set of routes.

## Features

- Async web server powered by `aiohttp` with CORS support.
- Feature-based structure: `bikes`, `boxes`, `carts`, `checkout`, `payments`, `auth`, `metadata`, and `status`.
- Firebase authentication via an optional auth middleware, with role concepts (admin / user / guest).
- PostgreSQL persistence using Peewee plus `psycopg2`.
- Stripe integration for payments.
- Auto-generated Swagger API docs.

## Tech Stack

| Area | Technology |
|------|------------|
| Language | Python 3.7+ |
| Web framework | aiohttp, aiohttp-cors, aiohttp-swagger |
| Auth / Cloud | Firebase Admin, Google Cloud Firestore |
| Database | PostgreSQL, Peewee, psycopg2 |
| Payments | Stripe |
| Container | Docker |
| CI | CircleCI |

## Getting Started

### Prerequisites

- Python 3.3+ and PIP 18+ (the Docker image uses Python 3.7).
- A PostgreSQL instance with a database named `bikeshop`.
- A Firebase application and service account file.

#### Prepare Firebase

1. Create a Firebase application.
2. Download a service account file.
3. Point to it via an environment variable:
   ```bash
   GOOGLE_APPLICATION_CREDENTIALS=path/to/service_account.json
   ```

#### Prepare PostgreSQL

For local development you can run Postgres in Docker:

```bash
docker run --rm --name pg-docker -e POSTGRES_PASSWORD=docker -d -p 5432:5432 \
  -v postgres-data:/var/lib/postgresql/data postgres
```

For an external database, set:

```bash
BIKESHOP_DATABASE=postgresql://user:pass@host:port/bikeshop
```

Create a database named `bikeshop` and run the schema in `infrastructure/relational_db/schema.db`.

### Installation

```bash
pip install -r requirements.txt
```

### Running

Start the app:

```bash
python server.py
```

For development, `nodemon` can auto-reload on changes (loading local credentials from `./__sensitive__/sa.json`):

```bash
GOOGLE_APPLICATION_CREDENTIALS=./__sensitive__/sa.json nodemon --exec "python3" server.py
```

Or run it in a container:

```bash
docker build -t bike_shop_api .
docker run -p 8082:8082 bike_shop_api
```

The server listens on port `8082`. Swagger docs are available at:

```
http://localhost:8082/api/doc
```

## Project Structure

```
bike_shop_api/
├── server.py            # App entry point — registers feature routes
├── config/              # CORS and app configuration
├── constants.py         # Shared enums/keys (roles, statuses, headers)
├── decorators/          # Reusable decorators
├── exceptions.py        # Custom exceptions
├── features/            # Feature modules (bikes, carts, payments, auth, ...)
├── helpers.py           # Shared helpers
├── infrastructure/      # DAL init and relational DB schema
├── middlewares/         # Auth middleware
└── Dockerfile
```
