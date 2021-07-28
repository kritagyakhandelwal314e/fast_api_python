from uuid import UUID
from utils import convert_to_key_value_pair, convert_to_key_value_pair_list, nested_values
from db.connection import conn
from datetime import datetime

async def get_all(pg_num: int, pg_size: int):
  limit = max(0, pg_size)
  skip = max(0, (pg_num - 1)) * pg_size
  with conn.cursor() as cur:
    cur.execute("""
    SELECT * FROM providers 
    ORDER BY provider_name
    LIMIT %s OFFSET %s;
    """, (limit, skip))
    conn.commit()
    return cur.fetchall()

async def get_searched(pg_num: int, pg_size: int, search_string: str):
  while len(search_string) and search_string[-1] == ' ':
    search_string = search_string[0:-1]
  search_query = ' | '.join(search_string.split(' '))
  limit = max(0, pg_size)
  skip = max(0, (pg_num - 1)) * pg_size
  with conn.cursor() as cur:
    cur.execute("""
    SELECT * FROM providers 
    WHERE provider_search_tokens @@ to_tsquery(%s)
    ORDER BY provider_name
    LIMIT %s OFFSET %s;
    """, (search_query, limit, skip))
    conn.commit()
    return cur.fetchall()

async def create_one(provider):
  search_string = ' '.join([str(value) for value in nested_values(provider.dict())])
  print(search_string)
  with conn.cursor() as cur:
    cur.execute("""
    SELECT org_id FROM organisations 
    WHERE org_name = %s 
    AND org_location = %s
    AND org_address = %s;
    """, (
      provider.provider_organisation.org_name,
      provider.provider_organisation.org_location,
      provider.provider_organisation.org_address
    ))
    record = cur.fetchone()
    if not record:
      print("organisation doesn't exist")
      cur.execute("""
      INSERT INTO organisations (
        org_name,
        org_location,
        org_address
      )
      VALUES (%s, %s, %s)
      RETURNING org_id;
      """, (
        provider.provider_organisation.org_name,
        provider.provider_organisation.org_location,
        provider.provider_organisation.org_address
      ))
      record = cur.fetchone()
    org_id = record[0]
    cur.execute("""
    INSERT INTO providers (
      provider_name, 
      provider_active, 
      provider_department,
      provider_org_id,
      provider_created_on,
      provider_last_modified_on, 
      provider_search_tokens
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    RETURNING *;
    """, (
      provider.provider_name, 
      provider.provider_active, 
      provider.provider_department, 
      org_id,
      datetime.now(),
      None,
      search_string
    ))
    provider_record = cur.fetchone()
    provider_id = provider_record[0]
    for p in provider.provider_phones:
      print(p)
      cur.execute("""
      SELECT phone_id FROM phones
      WHERE phone_country_code = %s
      AND phone_number = %s;
      """, (
        p.phone_country_code,
        p.phone_number
      ))
      record = cur.fetchone()
      if not record:
        print("phone doesn't exit")
        cur.execute("""
        INSERT INTO phones (
          phone_country_code,
          phone_number
        )
        VALUES (%s, %s)
        RETURNING phone_id;
        """, (
          p.phone_country_code,
          p.phone_number
        ))
        record = cur.fetchone()
      phone_id = record[0]
      cur.execute("""
      INSERT INTO provider_phone (
        provider_id, 
        phone_id
      ) 
      VALUES (%s, %s);
      """, (
        provider_id,
        phone_id
      ))
    for q in provider.provider_qualifications:
      print(q)
      cur.execute("""
      SELECT qual_id FROM qualifications
      WHERE qual_name = %s
      """, (
        q.qual_name,
      ))
      record = cur.fetchone()
      if not record:
        print("qualification doesn't exit")
        cur.execute("""
        INSERT INTO qualifications (
          qual_name
        )
        VALUES (%s)
        RETURNING qual_id;
        """, (
          q.qual_name,
        ))
        record = cur.fetchone()
      qual_id = record[0]
      cur.execute("""
      INSERT INTO provider_qualification (
        provider_id, 
        qual_id
      ) 
      VALUES (%s, %s);
      """, (
        provider_id,
        qual_id
      ))
    for s in provider.provider_specialities:
      print(s)
      cur.execute("""
      SELECT spec_id FROM specialities
      WHERE spec_name = %s
      """, (
        s.spec_name,
      ))
      record = cur.fetchone()
      if not record:
        print("speciality doesn't exit")
        cur.execute("""
        INSERT INTO specialities (
          spec_name
        )
        VALUES (%s)
        RETURNING spec_id;
        """, (
          s.spec_name,
        ))
        record = cur.fetchone()
      spec_id = record[0]
      cur.execute("""
      INSERT INTO provider_speciality (
        provider_id, 
        spec_id
      ) 
      VALUES (%s, %s);
      """, (
        provider_id,
        spec_id
      ))
    conn.commit()
    print(provider_record)
    return provider_record

async def get_one(provider_id: UUID):
  provider_id = str(provider_id)
  with conn.cursor() as cur:
    cur.execute("""
    SELECT * FROM providers
    WHERE provider_id = %s;
    """, (provider_id, ))
    provider = list(cur.fetchone())[:-1]
    if not provider:
      return None
    cur.execute("""
    SELECT org_name, org_location, org_address FROM organisations
    WHERE org_id = %s;
    """, (provider[4], ))
    organisation = await convert_to_key_value_pair(["org_name", "org_location", "org_address"], cur.fetchone())
    if not organisation:
      return None
    provider.append(organisation)
    cur.execute("""
    SELECT phone_country_code, phone_number 
    FROM provider_phone as pp
    JOIN phones as p
    ON pp.phone_id = p.phone_id
    WHERE pp.provider_id = %s;
    """, (provider_id, ))
    phones = await convert_to_key_value_pair_list(["phone_country_code", "phone_number"], cur.fetchall())
    provider.append(phones)
    cur.execute("""
    SELECT qual_name 
    FROM provider_qualification as pq
    JOIN qualifications as q
    ON pq.qual_id = q.qual_id
    WHERE pq.provider_id = %s;
    """, (provider_id, ))
    qualifications = await convert_to_key_value_pair_list(["qual_name"], cur.fetchall())
    provider.append(qualifications)
    cur.execute("""
    SELECT spec_name 
    FROM provider_speciality as ps
    JOIN specialities as s
    ON ps.spec_id = s.spec_id
    WHERE ps.provider_id = %s;
    """, (provider_id, ))
    specialities = await convert_to_key_value_pair_list(["spec_name"], cur.fetchall())
    provider.append(specialities)
    conn.commit()
    return provider

async def delete_one(provider_id: UUID):
  with conn.cursor() as cur:
    cur.execute("""
    DELETE FROM providers
    WHERE provider_id = %s;
    """, (str(provider_id), ))
    conn.commit()
  return None

async def update_one(provider_id: UUID, provider):
  provider_id = str(provider_id)
  search_string = ' '.join([str(value) for value in nested_values(provider.dict())])
  print(search_string)
  with conn.cursor() as cur:
    cur.execute("""
    DELETE FROM providers
    WHERE provider_id = %s
    RETURNING provider_created_on;
    """, (provider_id, ))
    provider_created_on = cur.fetchone()[0]
    cur.execute("""
    SELECT org_id FROM organisations 
    WHERE org_name = %s 
    AND org_location = %s
    AND org_address = %s;
    """, (
      provider.provider_organisation.org_name,
      provider.provider_organisation.org_location,
      provider.provider_organisation.org_address
    ))
    record = cur.fetchone()
    if not record:
      print("organisation doesn't exist")
      cur.execute("""
      INSERT INTO organisations (
        org_name,
        org_location,
        org_address
      )
      VALUES (%s, %s, %s)
      RETURNING org_id;
      """, (
        provider.provider_organisation.org_name,
        provider.provider_organisation.org_location,
        provider.provider_organisation.org_address
      ))
      record = cur.fetchone()
    org_id = record[0]
    cur.execute("""
    INSERT INTO providers (
      provider_name, 
      provider_active, 
      provider_department,
      provider_org_id,
      provider_created_on,
      provider_last_modified_on,
      provider_search_tokens
    )
    VALUES ( %s, %s, %s, %s, %s, %s, %s)
    RETURNING *;
    """, (
      provider.provider_name, 
      provider.provider_active, 
      provider.provider_department,
      org_id,
      provider_created_on,
      datetime.now(),
      search_string
    ))
    provider_record = cur.fetchone()
    provider_id = provider_record[0]
    for p in provider.provider_phones:
      print(p)
      cur.execute("""
      SELECT phone_id FROM phones
      WHERE phone_country_code = %s
      AND phone_number = %s;
      """, (
        p.phone_country_code,
        p.phone_number
      ))
      record = cur.fetchone()
      if not record:
        print("phone doesn't exit")
        cur.execute("""
        INSERT INTO phones (
          phone_country_code,
          phone_number
        )
        VALUES (%s, %s)
        RETURNING phone_id;
        """, (
          p.phone_country_code,
          p.phone_number
        ))
        record = cur.fetchone()
      phone_id = record[0]
      cur.execute("""
      INSERT INTO provider_phone (
        provider_id, 
        phone_id
      ) 
      VALUES (%s, %s);
      """, (
        provider_id,
        phone_id
      ))
    for q in provider.provider_qualifications:
      print(q)
      cur.execute("""
      SELECT qual_id FROM qualifications
      WHERE qual_name = %s
      """, (
        q.qual_name,
      ))
      record = cur.fetchone()
      if not record:
        print("qualification doesn't exit")
        cur.execute("""
        INSERT INTO qualifications (
          qual_name
        )
        VALUES (%s)
        RETURNING qual_id;
        """, (
          q.qual_name,
        ))
        record = cur.fetchone()
      qual_id = record[0]
      cur.execute("""
      INSERT INTO provider_qualification (
        provider_id, 
        qual_id
      ) 
      VALUES (%s, %s);
      """, (
        provider_id,
        qual_id
      ))
    for s in provider.provider_specialities:
      print(s)
      cur.execute("""
      SELECT spec_id FROM specialities
      WHERE spec_name = %s
      """, (
        s.spec_name,
      ))
      record = cur.fetchone()
      if not record:
        print("speciality doesn't exit")
        cur.execute("""
        INSERT INTO specialities (
          spec_name
        )
        VALUES (%s)
        RETURNING spec_id;
        """, (
          s.spec_name,
        ))
        record = cur.fetchone()
      spec_id = record[0]
      cur.execute("""
      INSERT INTO provider_speciality (
        provider_id, 
        spec_id
      ) 
      VALUES (%s, %s);
      """, (
        provider_id,
        spec_id
      ))
    conn.commit()
    return provider_record
