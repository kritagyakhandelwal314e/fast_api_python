async def convert_to_key_value_pair(key_list: list, val_list: list):
  return dict(zip(key_list, val_list))

async def convert_to_key_value_pair_list(key_list: list, val_list_list: list):
  res = []
  for val_list in val_list_list:
    res.append(await convert_to_key_value_pair(key_list, val_list))
  return res
