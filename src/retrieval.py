def retrieve_overviews(conn, bundle_ids):
  if bundle_ids == []:
    return []
  
  with conn.cursor() as cur:
    print(f"SELECT bundle_id, name, description, image_url FROM bundles WHERE bundle_id IN ({','.join(str(id) for id in bundle_ids)})")
    cur.execute(f"SELECT bundle_id, name, description, image_url FROM bundles WHERE bundle_id IN ({','.join(str(id) for id in bundle_ids)})")
    bundles = cur.fetchall()
    print("argument bundles", len(bundle_ids))
    print("bundles", len(bundles))

    ans = {
      b[0]: { 
        "bundle_id": b[0],
        "name": b[1],
        "description": b[2],
        "image_url": b[3]
      }
      for b in bundles 
    }

    return [ans[id] for id in bundle_ids]
  

def retrieve_bundle(conn, bundle_id):
  with conn.cursor() as cur:
    cur.execute("SELECT bundle_id, name, description, instructions, image_url FROM bundles WHERE bundle_id = %s", bundle_id)
    b = cur.fetchall()[0]

    cur.execute("SELECT ingredient, quantity FROM bundle_items WHERE bundle_id = %s", b[0])
    items = cur.fetchall()

    return {
      "bundle_id": b[0],
      "name": b[1],
      "description": b[2],
      "instructions": b[3],
      "image_url": b[4],
      "items": [{ "quantity": i[1], "product": { "product_id": hash(i[0]), "name": i[0], "price": 0, "base_price": 0 }} for i in items]
    }
