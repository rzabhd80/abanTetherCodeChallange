# ABAN Currency Order Processing Service

## Important Notice 
due to lack of time and meeting the deadline, Application services were not tested.


This project implements a financial service that handles placing and processing orders in ABAN currency, with specific
rules around small orders and bulk processing. It is built using Python, Celery, SQLAlchemy, and PostgreSQL, ensuring
robust transaction handling and task retry logic for failed tasks.



## Features

* **Order Accumulation:** Orders below $10 from multiple users are accumulated and processed as a single task.
* **Bulk Processing:** For multiple orders from different users, $4 is deducted from each user, and all orders are
  processed with a single call to `buy_from_exchange`.
* **Task Retry:** Failed tasks are retried using Celery's native retry mechanism.
* **PostgreSQL Transactions:** All database operations are handled in atomic transactions to ensure data consistency.

## Technologies

* **Python**: Core programming language for the service.
* **Celery**: Asynchronous task queue for handling long-running order processing tasks.
* **SQLAlchemy**: ORM for managing database transactions.
* **PostgreSQL**: Database for storing order and transaction data.

## API Overview

### Order Placement

Users can place orders using an API that takes:

1. **Amount**: The amount of ABAN currency to purchase.
2. **Currency**: (Hardcoded to ABAN).

The service calculates the amount based on user input and accumulates orders under $10 until the threshold is met. Once
accumulated, a single API call is made to `buy_from_exchange`.

### Accumulation Logic

* Orders with less than $10 are not immediately processed but instead accumulated.
* For larger or multiple orders, a $4 deduction is applied per order, and all are processed in bulk.

## Key Components

### `process_accumulated_orders` Task

This Celery task accumulates pending orders in ABAN currency and processes them together, ensuring that the API call
to `buy_from_exchange` is only made once for the accumulated amount.

```python
@celery_app.task(bind=True, max_retries=3, default_retry_delay=60)
def process_accumulated_orders(self):
    # Business logic to accumulate and process ABAN orders.
    pass
```

## Celery Task Status Tracking

Task status and retry logic are handled via Celery's built-in mechanisms, and order states are updated in PostgreSQL
using SQLAlchemy transactions.

## PostgreSQL Database Schema

**Orders**:  Stores information about placed orders, including status and amount.

**Task status**: Tracks the status of each Celery task, including retries and final outcomes.

## Running the Project

1. **Install Dependency**:

```bash
pip install -r requirements.txt
```

2. **Set up PostgreSQL database**: Make sure to configure the environment variables for the database connection.

3. **Run Celery workers:**

```bash 
celery -A <project_name> worker --loglevel=info
```

# known issues

Due to time constraints, application services were not tested. While a Dockerfile and a Compose setup
are provided, further validation is needed to ensure proper deployment
