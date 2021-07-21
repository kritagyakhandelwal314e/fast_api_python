from starlette.responses import JSONResponse
from psycopg2.errors import UniqueViolation
import functools

def handle(func):
  @functools.wraps(func)
  async def wrapper_decorator(*args, **kwargs):
    try:
      return await func(*args, **kwargs)
    except UniqueViolation as error:
      print(error.__repr__())
      return JSONResponse(status_code=409, content={"message": "record Uniqueness conflict"})
    except Exception as error:
      print(error.__repr__())
      return server_error
  return wrapper_decorator

async def convert_to_key_value_pair(key_list: list, val_list: list):
  return dict(zip(key_list, val_list))

async def convert_to_key_value_pair_list(key_list: list, val_list_list: list):
  res = []
  for val_list in val_list_list:
    res.append(await convert_to_key_value_pair(key_list, val_list))
  return res

not_implemented =  JSONResponse(status_code=501, content={"message": "Method not implemented"})
server_error = JSONResponse(status_code=500, content={"message": "Server Error"})
not_found = JSONResponse(status_code=404, content={"message": "Not Found"})

