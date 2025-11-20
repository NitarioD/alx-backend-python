#!/usr/bin/python3
"""
Batch processing of users from user_data table in ALX_prodev
"""

import mysql.connector
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def get_db_config():
    """Get database configuration from environment variables"""
    return {
        'host': os.getenv('DB_HOST', 'localhost'),
        'user': os.getenv('DB_USER', 'root'),
        'password': os.getenv('DB_PASSWORD', ''),
        'database': os.getenv('DB_NAME', 'ALX_prodev'),
        'port': os.getenv('DB_PORT', '3306')
    }

def stream_users_in_batches(batch_size):
    """
    Generator that yields rows in batches of size batch_size
    """
    connection = None
    cursor = None
    try:
        config = get_db_config()
        
        # Fixed: Proper indentation for multiple with statements
        with mysql.connector.connect(**config) as connection:
            with connection.cursor(dictionary=True) as cursor:
                cursor.execute("SELECT * FROM user_data;")
                while True:
                    batch = cursor.fetchmany(batch_size)
                    if not batch:
                        break
                    yield batch

    except mysql.connector.Error as e:
        print(f"Database error: {e}")
    finally:
        # The with statements will handle closing, but keep this as backup
        if cursor and not cursor.close:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()

def batch_processing(batch_size):
    """
    Processes each batch and prints users over age 25
    """
    for batch in stream_users_in_batches(batch_size):          # loop 1
        for user in batch:                                     # loop 2
            # Convert age from Decimal to int if needed
            age = user["age"]
            if hasattr(age, 'to_integral_value'):
                age = int(age)
            if age > 25:
                print(user)