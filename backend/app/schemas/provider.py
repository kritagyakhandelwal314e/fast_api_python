from pydantic import BaseModel, Field
from typing import Optional, List
from .phone import Phone
from .speciality import Speciality
from .qualification import Qualification
from .organisation import Organisation
from datetime import datetime

class Provider(BaseModel):
  provider_name: str = Field(min_length=3, max_length=64)
  provider_active: bool = True
  provider_qualifications: List[Qualification] = Field(min_items=1)
  provider_specialities: List[Speciality] = Field(min_items=1)
  provider_phones: List[Phone] = Field(min_items=1)
  provider_organisation: Organisation
  provider_street_address: str = Field(min_length=3, max_length=64)
  provider_city: str = Field(min_length=3, max_length=64)
  provider_state: str = Field(min_length=3, max_length=64)
  provider_country: str = Field(min_length=3, max_length=64)
  provider_zipcode: str = Field(min_length=3, max_length=64, regex=r'[0-9]{6}')
  provider_created_on: Optional[datetime]
  provider_modified_on: Optional[datetime]




