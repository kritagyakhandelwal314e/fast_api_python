from enum import unique
from faker import Faker
from random import randint
from pprint import pprint

def gen_data():
  fake = Faker()

  qualifications_list = ['BTech', 'MTech', 'Phd', 'BSc', 'MBA', 'MS', 'MSc', 'MCom']
  specialities_list = ["Aerospace Medicine", "Anaesthesia", "Bariatric Surgery", "Cardiology - Interventional", "Cardiology - Non Interventional", "Cardiothoracic And Vascular Surgery", "Centre For Spinal Diseases", "Clinical Haematology And BMT", "Corneal Transplant", "Critical Care Medicine", "Dermatology And Cosmetology", "Ear Nose Throat Head And Neck Surgery", "Emergency Medicine", "Endocrinology", "General Surgery", "Infectious Diseases", "Internal Medicine", "In-Vitro Fertilisation (IVF)", "Laboratory Medicine", "Liver Transplant & Hepatic Surgery", "Maxillofacial Surgery", "Medical Gastroenterology", "Medical Oncology & Clinical Hematology", "Medical Oncology", "Minimally Invasive Gynecology", "Neonatology", "Nephrology", "Neuro Modulation", "Nutrition & Dietetics", "Neurology", "Neurosurgery", "Obstetrics And Gynecology", "Ophthalmology", "Orthopedics & Joint Replacement", "Pain Management", "Pediatric Surgery", "Physiotherapy", "Plastic Surgery", "Psychiatry", "Pulmonology", "Renal Transplant", "Reproductive Medicine & IVF", "Rheumatology", "Robotic Surgery", "Surgical Gastroenterology", "Surgical Oncology", "Urology", "Vascular and endovascular surgery"]
  departments_list = ["OPD", "OT", "Emergency", "Management"]
  data = {}

  data['provider_name'] = fake.name()
  data['provider_active'] = fake.pybool()
  qualifications = fake.random_elements(
    elements=qualifications_list,
    unique=True,
    length=randint(1, 6)
  )
  data['provider_qualifications'] = []
  for qual_name in qualifications:
    data['provider_qualifications'].append({
      'qual_name': qual_name
    })
  specialities = fake.random_elements(
    elements=specialities_list,
    unique=True,
    length=randint(1, 8)
  )
  data['provider_specialities'] = []
  for spec_name in specialities:
    data['provider_specialities'].append({
      'spec_name': spec_name
    })
  data['provider_phones'] = []
  for i in range(randint(1, 4)):
    data['provider_phones'].append({
      'phone_country_code': '+' + fake.numerify(text='##'),
      'phone_number': fake.numerify(text='#'*randint(8, 10))
    })
  data['provider_organisation'] = {
    'org_name': fake.company(),
    'org_location': fake.city(),
    'org_address': 'address'
  }
  data['provider_department'] = fake.random_element(elements=departments_list)
  return data