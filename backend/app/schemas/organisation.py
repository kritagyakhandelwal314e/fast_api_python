from pydantic import BaseModel, Field
from typing import Optional

class Organisation(BaseModel):
  org_name: str = Field(min_length=3, max_length=64)
  org_location: Optional[str] = Field(None, min_length=3, max_length=64)
  org_address: str = Field(min_length=3, max_length=256)
