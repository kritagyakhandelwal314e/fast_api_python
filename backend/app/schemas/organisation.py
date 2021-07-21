from pydantic import BaseModel, Field
from typing import Optional, List

class Organisation(BaseModel):
  org_name: str = Field(min_length=3, max_length=64)
  org_location: Optional[str] = Field(None, min_length=3, max_length=64)

class OrganisationAllOptional(BaseModel):
  org_name: Optional[str] = Field(min_length=3, max_length=64)
  org_location: Optional[str] = Field(min_length=3, max_length=64)
