#!/usr/bin/python3
"""
Memory-efficient aggregation using generators:
Compute average age of users without loading entire dataset
"""

import seed


def stream_user_ages():
    """
    Generator that yields user ages one by one
    """
    connection = None
    cursor = None
    try:
        connection = seed.connect_to_prodev()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT age FROM user_data;")
        for row in cursor:   # ✅ loop 1
            yield row["age"]
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


def average_age():
    """
    Calculate average age using generator without loading all data
    """
    total = 0
    count = 0
    for age in stream_user_ages():   # ✅ loop 2
        total += age
        count += 1
    if count == 0:
        return 0
    return total / count


if __name__ == "__main__":
    avg = average_age()
    print(f"Average age of users: {avg:.2f}")
