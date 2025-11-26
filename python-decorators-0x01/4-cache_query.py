#!/usr/bin/python3
"""
Decorator to cache query results to avoid redundant database calls
"""

import sqlite3
import functools

# In-memory cache
query_cache = {}


def with_db_connection(func):
    """
    Decorator that opens a database connection,
    passes it to the function, and closes it afterward
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect("users.db")
        try:
            result = func(conn, *args, **kwargs)
            return result
        finally:
            conn.close()
    return wrapper


def cache_query(func):
    """
    Decorator that caches query results based on the SQL query string.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Extract query string from kwargs or args
        query = kwargs.get("query") or (args[1] if len(args) > 1 else None)
        if query in query_cache:
            print(f"Using cached result for query: {query}")
            return query_cache[query]

        # Execute function and cache result
        result = func(*args, **kwargs)
        query_cache[query] = result
        print(f"Caching result for query: {query}")
        return result
    return wrapper


@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()


# Example usage
if __name__ == "__main__":
    # First call will hit DB and cache result
    users = fetch_users_with_cache(query="SELECT * FROM users")
    print(users)

    # Second call will fetch from cache instead of DB
    users_again = fetch_users_with_cache(query="SELECT * FROM users")
    print(users_again)