# Python Context Managers & Async Operations

This directory contains Python scripts that demonstrate how to use context managers and asynchronous programming with databases.

## Files

### 0-databaseconnection.py
- Implements a **class-based context manager** `DatabaseConnection` using `__enter__` and `__exit__`.
- Handles opening and closing SQLite database connections automatically.
- Example: Fetch all users from the `users` table.

### 1-execute.py
- Implements a **reusable context manager** `ExecuteQuery` that:
  - Accepts a query and parameters.
  - Executes the query and returns results.
- Example: Fetch users older than 25.

### 3-concurrent.py
- Demonstrates running multiple **asynchronous queries** concurrently using `aiosqlite` and `asyncio.gather`.
- Functions:
  - `async_fetch_users()` → fetch all users.
  - `async_fetch_older_users()` → fetch users older than 40.
- Uses `asyncio.run()` to execute concurrent tasks.

## Requirements
- Python 3.8+
- SQLite
- [aiosqlite](https://pypi.org/project/aiosqlite/)

Install dependencies:
```bash
pip install aiosqlite
```

## Running the Scripts
```bash
python3 0-databaseconnection.py
python3 1-execute.py
python3 3-concurrent.py
```