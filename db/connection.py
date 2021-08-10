import psycopg2
import pprint

# Connect to your postgres DB -> cursor
def connect_db():
  conn = psycopg2.connect("postgresql://fastapi_traefik:fastapi_traefik@db:5432/healthcaredb")
  return conn

conn = connect_db()