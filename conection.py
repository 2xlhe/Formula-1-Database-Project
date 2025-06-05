import hashlib
import psycopg2
from psycopg2 import sql
import getpass
import os

#Efetua conexão à base de dados
def conecta_banco():
    connection = psycopg2.connect(host="localhost", port="5432",
                                  dbname="fia", user="postgres", password="postgres")
    cursor = connection.cursor()
    return connection, cursor
