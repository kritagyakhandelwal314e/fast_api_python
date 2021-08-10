from pydantic import BaseModel, Field
from typing import Optional, List

class Speciality(BaseModel):
  spec_name: str = Field(min_length=2, max_length=64)
