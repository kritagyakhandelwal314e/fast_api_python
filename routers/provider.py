from uuid import UUID
from schemas.provider import Provider
from fastapi import APIRouter
from db.provider import get_all, create_one, get_one, delete_one, get_searched, update_one
from utils import convert_to_key_value_pair, convert_to_key_value_pair_list, handle, not_implemented, not_found

router = APIRouter(
  prefix="/api/providers",
  tags=["provider"]
)

columns = [
  "provider_id", 
  "provider_name", 
  "provider_active", 
  "provider_department",
  "provider_org_id",
  "provider_created_on",
  "provider_last_modified_on"
]

columns_extended = [
  "provider_id", 
  "provider_name", 
  "provider_active", 
  "provider_department",
  "provider_org_id",
  "provider_created_on",
  "provider_last_modified_on",
  "provider_organisation",
  "provider_phones",
  "provider_qualifications",
  "provider_specialities"
]

@router.get("/")
@handle
async def get_providers(pg_num: int = 1, pg_size: int = 10):
  records = await get_all(pg_num, pg_size)
  return await convert_to_key_value_pair_list(columns, records)
  

@router.post("/", status_code=201)
@handle
async def post_providers(provider: Provider):
  record =  await create_one(provider=provider)
  return await convert_to_key_value_pair(columns, record)

@router.delete("/", status_code=202)
@handle
async def delete_providers():
  return not_implemented

@router.put("/")
@handle
async def put_providers():
  return not_implemented

@router.patch("/")
@handle
async def patch_providers():
  return not_implemented

@router.get("/search")
@handle
async def search_provider(pg_num: int = 1, pg_size: int = 10, search_string: str = ''):
  if not search_string:
    records = await get_all(pg_num=pg_num, pg_size=pg_size)
    return await convert_to_key_value_pair_list(columns, records)
  else:
    records = await get_searched(pg_num=pg_num, pg_size=pg_size, search_string=search_string)
    return await convert_to_key_value_pair_list(columns, records)

@router.get("/{provider_id}")
@handle
async def get_provider(provider_id: UUID):
  record = await get_one(provider_id)
  if not record:
    return not_found
  return await convert_to_key_value_pair(columns_extended, record)

@router.post("/{provider_id}")
@handle
async def post_provider(provider_id: UUID):
  return not_implemented

@router.delete("/{provider_id}", status_code=202)
# @handle
async def delete_provider(provider_id: UUID):
  print(type(provider_id))
  return await delete_one(provider_id)

@router.put("/{provider_id}")
@handle
async def put_provider(provider_id: UUID, provider: Provider):
  record = await update_one(provider_id=provider_id, provider=provider)
  return await convert_to_key_value_pair(columns, record)

@router.patch("/{provider_id}")
@handle
async def patch_provider(provider_id: UUID):
  return not_implemented

