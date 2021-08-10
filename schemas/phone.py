from pydantic import BaseModel, Field
from typing import Optional, List

class Phone(BaseModel):
  phone_country_code: str = Field('+91', max_length=3, regex=r'^\+[0-9][0-9]')
  phone_number: str = Field(regex=r'[0-9]{8,10}', min_length=8, max_length=10)