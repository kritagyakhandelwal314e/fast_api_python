from schemas.organisation import Organisation, OrganisationAllOptional
from fastapi import APIRouter
from db.organisation import create_one, delete_one, get_all, get_one, delete_all, update_one
from utils import convert_to_key_value_pair, convert_to_key_value_pair_list, handle, not_implemented, not_found

router = APIRouter(
  prefix="/api/organisations",
  tags=["organisation"]
)

columns = ["org_id", "org_name", "org_location"]

@router.get("/")
@handle
async def get_organisations(pg_num: int = 1, pg_size: int = 10):
  records = await get_all(pg_num, pg_size)
  return await convert_to_key_value_pair_list(columns, records)
  

@router.post("/", status_code=201)
@handle
async def post_organisations(organisation: Organisation):
  return await create_one(organisation=organisation)

@router.delete("/", status_code=202)
@handle
async def delete_organisations():
  return await delete_all()

@router.put("/")
@handle
async def put_organisations():
  return not_implemented

@router.patch("/")
@handle
async def patch_organisations():
  return not_implemented

@router.get("/{org_id}")
@handle
async def get_organisation(org_id: int):
  record = await get_one(org_id)
  if not record:
    return not_found
  return await convert_to_key_value_pair(columns, record)

@router.post("/{org_id}")
@handle
async def post_organisation(org_id: int):
  return not_implemented

@router.delete("/{org_id}", status_code=202)
@handle
async def delete_organisation(org_id: int):
  return await delete_one(org_id=org_id)

@router.put("/{org_id}")
@handle
async def put_organisation(org_id: int, organisation: Organisation):
  record = await update_one(org_id=org_id, organisation=organisation)
  return await convert_to_key_value_pair(columns, record)

@router.patch("/{org_id}")
@handle
async def patch_organisation(org_id: int, organisation: OrganisationAllOptional):
  return not_implemented
