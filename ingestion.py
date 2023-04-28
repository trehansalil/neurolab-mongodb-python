import requests
import sys
import configparser
import json

from gsheet import *

sheet_name = variable_extractor('sheet_name', var_type='string')

url = f"{g_sheets_url}?sheetName={sheet_name}"
# print(url)
data = json.loads(requests.get(url).text)

if sheet_name==sheet_name1:
    coll = db[mongo_db_coll_procedure_risk]
    coll_backup = db_backup[mongo_db_coll_procedure_risk]
elif sheet_name==sheet_name2:
    coll = db[mongo_db_coll_sun_sensitivity]
    coll_backup = db_backup[mongo_db_coll_sun_sensitivity]
elif sheet_name==sheet_name3:
    coll = db[mongo_db_coll_hq]
    coll_backup = db_backup[mongo_db_coll_hq]
elif sheet_name==sheet_name4:
    coll = db[mongo_db_coll_retinol]
    coll_backup = db_backup[mongo_db_coll_retinol]
else:
    print('No Collection Created')
j = 1
for i in tqdm(data[:-1]):

    i['created_on'] = datetime.now()
    i['updated_on'] = datetime.now()

    if 'coll' in locals():
        if j==1:
            if drop_coll_bool:
                if coll.count_documents({})>0:
                    # result = list()
                    coll_backup.insert_many(coll.find())
                coll.drop()

            coll.insert_one(i)
            j+=1
        else:
            coll.insert_one(i)
            j+=1