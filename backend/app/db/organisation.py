from db.connection import conn

async def create_one(organisation):
  try:
    with conn.cursor() as cur:
      cur.execute("""
        INSERT INTO organisations (org_name, org_location)
        VALUES (%s, %s);
        """, (organisation.org_name, organisation.org_location))
      conn.commit()
      return organisation
  except Exception as error:
    raise error
  
async def get_all(pg_num: int, pg_size: int):
  try:
    limit = max(0, pg_size)
    skip = max(0, (pg_num - 1)) * pg_size
    with conn.cursor() as cur:
      cur.execute("""
      SELECT * FROM organisations LIMIT %s OFFSET %s;
      """, (limit, skip))
      conn.commit()
      return cur.fetchall()
  except Exception as error:
    raise error