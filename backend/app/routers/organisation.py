from schemas.organisation import Organisation
from starlette.responses import JSONResponse
from psycopg2.errors import UniqueViolation
from fastapi import APIRouter
from db.organisation import create_one, get_all
from utils import convert_to_key_value_pair, convert_to_key_value_pair_list

router = APIRouter(
  prefix="/api/organisations",
  tags=["organisation"]
)

@router.get("/")
async def get_organisations(pg_num: int = 1, pg_size: int = 10):
  try:
    records = await get_all(pg_num, pg_size)
    return await convert_to_key_value_pair_list(["org_id", "org_name", "org_location"], records)
  except Exception as error:
    print(error)
    return JSONResponse(status_code=500, content={"message": "Server Error"})

@router.post("/", status_code=201)
async def post_organisations(organisation: Organisation):
  try:
    return await create_one(organisation=organisation)
  except UniqueViolation as error:
    print(error.__repr__(), type(error))
    return JSONResponse(status_code=409, content={"message": "record Uniqueness conflict"})
  except Exception as error:
    return JSONResponse(status_code=500, content={"message": "Server Error"})