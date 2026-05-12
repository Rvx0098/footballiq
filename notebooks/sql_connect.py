import mysql.connector
import pandas as pd

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Rvsql0987",
    database="footballiq"
)

print("Connected!")