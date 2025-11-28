import sqlite3
from typing import Any, List, Tuple


class ExecuteQuery:
    """
    A reusable context manager that handles database connection and query execution.
    It takes a query and optional parameters, executes the query, and returns results.
    """

    def __init__(self, db_name: str, query: str, params: Tuple[Any, ...] = ()):
        self.db_name = db_name
        self.query = query
        self.params = params
        self.connection = None
        self.cursor = None
        self.results: List[Tuple[Any, ...]] = []

    def __enter__(self):
        """Open connection, execute the query, and return the results."""
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()
        self.cursor.execute(self.query, self.params)
        # fetch results if it's a SELECT query
        if self.query.strip().upper().startswith("SELECT"):
            self.results = self.cursor.fetchall()
        else:
            self.connection.commit()
        return self.results

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Close cursor and connection."""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        return False  # don't suppress exceptions


if __name__ == "__main__":
    # Setup: create table & insert users
    with sqlite3.connect("example.db") as conn:
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)")
        c.execute("INSERT INTO users (name, age) VALUES (?, ?)", ("Alice", 30))
        c.execute("INSERT INTO users (name, age) VALUES (?, ?)", ("Bob", 22))
        c.execute("INSERT INTO users (name, age) VALUES (?, ?)", ("Charlie", 28))
        conn.commit()

    # Example usage of ExecuteQuery
    query = "SELECT * FROM users WHERE age > ?"
    with ExecuteQuery("example.db", query, (25,)) as results:
        for row in results:
            print(row)