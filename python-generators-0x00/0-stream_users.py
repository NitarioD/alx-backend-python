#!/usr/bin/python3
"""
Generator that streams rows from user_data table in ALX_prodev database
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

def stream_users():
    """Generator that yields rows from user_data one by one"""
    connection = None
    cursor = None
    try:
        config = get_db_config()
        connection = mysql.connector.connect(**config)
        
        # Use buffered cursor to avoid unread result issues
        cursor = connection.cursor(buffered=True, dictionary=True)

        cursor.execute("SELECT * FROM user_data;")
        
        # Convert age from Decimal to int for cleaner output
        for row in cursor:
            if 'age' in row and hasattr(row['age'], 'to_integral_value'):
                row['age'] = int(row['age'])
            yield row

    except mysql.connector.Error as e:
        print(f"Database error: {e}")
    finally:
        # Properly close resources
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()

# Make the module callable
import sys

class CallableModule(type(sys)):
    def __call__(self):
        return stream_users()

sys.modules[__name__].__class__ = CallableModule