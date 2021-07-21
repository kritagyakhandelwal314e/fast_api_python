from db.connection import conn

async def get_all(pg_num: int, pg_size: int):
  limit = max(0, pg_size)
  skip = max(0, (pg_num - 1)) * pg_size
  with conn.cursor() as cur:
    cur.execute("""
    SELECT * FROM organisations LIMIT %s OFFSET %s;
    """, (limit, skip))
    conn.commit()
    return cur.fetchall()

async def create_one(organisation):
  with conn.cursor() as cur:
    cur.execute("""
    INSERT INTO organisations (org_name, org_location)
    VALUES (%s, %s);
    """, (organisation.org_name, organisation.org_location))
    conn.commit()
    return organisation

async def delete_all():
  with conn.cursor() as cur:
    cur.execute("""
    DELETE FROM organisations;
    """)
    conn.commit()
    return None

async def get_one(org_id: int):
  with conn.cursor() as cur:
    cur.execute("""
    SELECT * FROM organisations WHERE org_id = %s;
    """, (str(org_id)))
    conn.commit()
    return cur.fetchone()

async def update_one(org_id: int, organisation):
  with conn.cursor() as cur:
    cur.execute("""
    UPDATE organisations 
    SET org_name = %s, 
    org_location = %s
    WHERE org_id = %s
    RETURNING *;""", (
      organisation.org_name, 
      organisation.org_location, 
      org_id
      )
    )
    conn.commit()
    return cur.fetchone()

async def delete_one(org_id: int):
  with conn.cursor() as cur:
    cur.execute("""
    DELETE FROM organisations 
    WHERE org_id = %s;
    """, (str(org_id)))
    conn.commit()
    return None
