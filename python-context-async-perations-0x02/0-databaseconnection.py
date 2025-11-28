import sqlite3


class DatabaseConnection:
    """Custom context manager to handle database connections."""

    def __init__(self, db_name: str):
        self.db_name = db_name
        self.connection = None

    def __enter__(self):
        self.connection = sqlite3.connect(self.db_name)
        return self.connection

    def __exit__(self, exc_type, exc_value, traceback):
        if self.connection:
            self.connection.close()


if __name__ == "__main__":
    db_file = "example.db"

    # Create a demo table and insert data
    with DatabaseConnection(db_file) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)"
        )
        cursor.execute("DELETE FROM users")  # clear old data
        cursor.executemany(
            "INSERT INTO users (name, age) VALUES (?, ?)",
            [
                ("Alice", 30),
                ("Bob", 22),
                ("Charlie", 45),
            ],
        )
        conn.commit()

    # Use context manager to fetch users
    with DatabaseConnection(db_file) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()
        print("Users:", rows)