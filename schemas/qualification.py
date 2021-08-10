from pydantic import BaseModel, Field
from typing import Optional, List

class Qualification(BaseModel):
  qual_name: str = Field(min_length=2, max_length=64)
