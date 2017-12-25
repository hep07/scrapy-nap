import json

data = open("./mytest/nap_us_vg_gg_dm_ar_je_vi_al_ua/nap_multiple.json").read()
json_data = json.loads(data)

len(json_data)

product_code_read = sorted([int(x["product_code"]) for x in json_data])
len(list(set(product_code_read)))


data = open("./mytest/nap_gg_p21.json").read()
json_data = json.loads(data)

len(json_data)

json_data[0]['product_code']