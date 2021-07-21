from pydantic import BaseModel, Field
from typing import Optional, List

class Phone(BaseModel):
  country_code: str = Field('+91', max_length=3, regex=r'^\+[0-9][0-9]')
  number: str = Field(regex=r'[0-9]{8,10}', min_length=8, max_length=10)