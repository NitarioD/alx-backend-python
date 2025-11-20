#!/usr/bin/python3
"""
Seed script for ALX_prodev MySQL database
"""

import mysql.connector
from mysql.connector import Error
import csv
import uuid
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def get_db_config(include_database=True):
    """Get database configuration from environment variables"""
    config = {
        'host': os.getenv('DB_HOST', 'localhost'),
        'user': os.getenv('DB_USER', 'root'),
        'password': os.getenv('DB_PASSWORD', ''),
        'port': os.getenv('DB_PORT', '3306')
    }
    
    if include_database:
        config['database'] = os.getenv('DB_NAME', 'ALX_prodev')
    
    return config

def connect_db():
    """Connects to MySQL server (not to a specific DB)"""
    try:
        config = get_db_config(include_database=False)

        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None


def create_database(connection):
    """Creates ALX_prodev database if it does not exist"""
    try:
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev;")
        cursor.close()
    except Error as e:
        print(f"Error creating database: {e}")


def connect_to_prodev():
    """Connects directly to ALX_prodev database"""
    try:
        config = get_db_config(include_database=True)

        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error connecting to ALX_prodev: {e}")
        return None


def create_table(connection):
    """Creates user_data table if it does not exist"""
    try:
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_data (
                user_id VARCHAR(36) PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                age DECIMAL NOT NULL,
                INDEX(user_id)
            );
        """)
        connection.commit()
        cursor.close()
        print("Table user_data created successfully")
    except Error as e:
        print(f"Error creating table: {e}")


def insert_data(connection, csv_file):
    """Insert CSV data into user_data if not already inserted"""
    try:
        cursor = connection.cursor()

        with open(csv_file, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                user_id = str(uuid.uuid4())
                name = row["name"]
                email = row["email"]
                age = row["age"]

                # Check if email already exists (to avoid duplicates)
                cursor.execute("SELECT * FROM user_data WHERE email = %s", (email,))
                if cursor.fetchone():
                    continue

                cursor.execute(
                    "INSERT INTO user_data (user_id, name, email, age) VALUES (%s, %s, %s, %s)",
                    (user_id, name, email, age)
                )

        connection.commit()
        cursor.close()
    except Error as e:
        print(f"Error inserting data: {e}")