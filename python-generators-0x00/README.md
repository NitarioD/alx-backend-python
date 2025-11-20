# Python Generators – 0x00

## Project Overview

This project demonstrates how to use **Python generators** for memory-efficient operations with a MySQL database.  
It covers streaming, batch processing, lazy pagination, and aggregation without loading entire datasets into memory.

The project uses a sample `user_data.csv` file to populate a MySQL database (`ALX_prodev`) with user records.

---

## Project Structure

```
python-generators-0x00/
│
├── seed.py # Setup script: creates DB, table, inserts CSV data
├── 0-stream_users.py # Generator streaming rows one by one
├── 1-batch_processing.py # Batch processing generator
├── 2-lazy_paginate.py # Lazy pagination with generators
├── 4-stream_ages.py # Memory-efficient average age calculator
│
├── 0-main.py # Test script for database setup
├── 1-main.py # Test script for streaming rows
├── 2-main.py # Test script for batch processing
├── 3-main.py # Test script for lazy pagination
├── user_data.csv # Sample dataset
└── README.md # Project documentation
```

---

## Requirements

- Python 3.8+
- MySQL Server
- Python MySQL connector
  ```bash
  pip install mysql-connector-python
  ```

---

## Tasks

### 0. Stream Users

File: 0-stream_users.py

Function: stream_users()

Description: Streams rows from the user_data table one by one.

Run:

```bash
./1-main.py
```

---

### 1. Batch Processing Large Data

- File: 1-batch_processing.py
- Functions:
- - stream_users_in_batches(batch_size) → fetches rows in chunks
- - batch_processing(batch_size) → filters users over age 25
- Description: Processes large datasets efficiently in batches.

Run:

```bash
./2-main.py | head -n 5
```

---

### 2. Lazy Loading Paginated Data

- File: 2-lazy_paginate.py
- Functions:
- - paginate_users(page_size, offset) → fetches a page from DB
- - lazy_pagination(page_size) → lazily yields pages one by one
- Description: Simulates pagination without preloading everything.

Run:

```bash
./3-main.py | head -n 7
```

---

### 3. Memory-Efficient Aggregation

- File: 4-stream_ages.py
- Functions:
- - stream_user_ages() → yields ages one at a
- - average_age() → computes average age with O(1) memory
- Description: Uses generators to calculate average age of users.

Run:

```bash
python3 4-stream_ages.py
```

Output:

```bash
Average age of users: 58.73
```

## Author

Adunola Mojolaoluwa
