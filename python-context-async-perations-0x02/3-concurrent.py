import asyncio
import aiosqlite


async def async_fetch_users():
    """Fetch all users asynchronously from the database."""
    async with aiosqlite.connect("example.db") as db:
        async with db.execute("SELECT * FROM users") as cursor:
            rows = await cursor.fetchall()
            print("All Users:", rows)
            return rows


async def async_fetch_older_users():
    """Fetch users older than 40 asynchronously from the database."""
    async with aiosqlite.connect("example.db") as db:
        async with db.execute("SELECT * FROM users WHERE age > 40") as cursor:
            rows = await cursor.fetchall()
            print("Users older than 40:", rows)
            return rows


async def fetch_concurrently():
    """Run multiple fetch queries concurrently using asyncio.gather."""
    results = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )
    return results


if __name__ == "__main__":
    # Ensure DB has some test data
    async def setup_db():
        async with aiosqlite.connect("example.db") as db:
            await db.execute(
                "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)"
            )
            await db.execute("DELETE FROM users")
            await db.executemany(
                "INSERT INTO users (name, age) VALUES (?, ?)",
                [
                    ("Alice", 30),
                    ("Bob", 22),
                    ("Charlie", 45),
                    ("Diana", 50),
                ],
            )
            await db.commit()

    asyncio.run(setup_db())
    asyncio.run(fetch_concurrently())