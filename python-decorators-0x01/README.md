# Python Decorators - 0x01

This project demonstrates the use of Python decorators to enhance database operations.  
The tasks focus on building custom decorators for logging, caching, retrying, and connection handling.

## Files

- **0-log_queries.py**  
  Adds a `log_queries` decorator that logs SQL queries with a timestamp before execution.

- **1-with_db_connection.py**  
  Implements `with_db_connection` decorator to handle opening and closing SQLite database connections automatically.

- **2-measure_time.py**  
  Implements a `measure_time` decorator that measures the execution time of database queries.

- **3-retry_on_failure.py**  
  Adds `retry_on_failure` decorator that retries database operations in case of transient failures.

- **4-cache_query.py**  
  Adds `cache_query` decorator that caches query results to avoid redundant database calls.

## Usage

Run the scripts directly with Python 3:

```bash
python3 0-log_queries.py
```

Each script connects to a sample SQLite database (users.db) and demonstrates the decorator in action.

## Requirements

- Python 3.x
- SQLite3

## Author

Adunola Mojolaoluwa
