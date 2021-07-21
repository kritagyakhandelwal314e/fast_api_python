from db.connection import conn

async def get_all(pg_num: int, pg_size: int):
  limit = max(0, pg_size)
  skip = max(0, (pg_num - 1)) * pg_size
  with conn.cursor() as cur:
    cur.execute("""
    SELECT * FROM providers LIMIT %s OFFSET %s;
    """, (limit, skip))
    conn.commit()
    return cur.fetchall()

async def create_one(provider):
  with conn.cursor() as cur:
    cur.execute("""
    INSERT INTO providers (
      provider_name, 
      provider_active, 
      provider_department,
      provider_org_id,
      provider_street_address,
      provider_city,
      provider_state,
      provider_country,
      provider_zipcode,
      provider_created_on,
      provider_last_modified_on
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, NOW(), None)
    RETURNING *;
    """, (
      provider.provider_name, 
      provider.provider_active, 
      provider.provider_department,
      provider.provider_org_id,
      provider.provider_street_address,
      provider.provider_city,
      provider.provider_state,
      provider.provider_country,
      provider.provider_zipcode,
    ))
    conn.commit()
    return provider