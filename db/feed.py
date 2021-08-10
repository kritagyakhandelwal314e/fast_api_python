import requests
from data import gen_data
import json

feeds = 5
while feeds:
  try:
    d = gen_data()
    response = requests.post('http://127.0.0.1:8000/api/providers', json=d )
    feeds -= 1
  except Exception as e:
    print(e)