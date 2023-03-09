import json
import requests
import subprocess
from bs4 import BeautifulSoup
import glob
import pandas as pd

cookie = 'MAIN_COOKIE_KEY=aa9895dbd004d4c957adecb0ba438cb6c201a13f64784fde340057658e233b57-u=sbansal%40gsma.com&t=1678347953543;'
def fetch_excel_data(org_id, country, org_name):
    # print("Org ID: ", org_id)
    # print(cookie)
    subprocess.run(["mkdir", country], stderr=subprocess.PIPE, text=True)
    result = subprocess.run(["sh", "main.sh", f"{org_id}", cookie, country, org_name], stderr=subprocess.PIPE, text=True)



    print(result.stderr)

def integrate_data(country):
    filenames = glob.glob(country + "/*.xlsx")
    print('File names:', filenames)
    # Initializing empty data frame
    finalexcelsheet = pd.DataFrame()
    for file in filenames:
        # combining multiple excel worksheets 
        # into single data frames
        df = pd.concat(pd.read_excel(file, sheet_name=None, skiprows=2),
                    ignore_index=True, sort=False).dropna()
        attr_id = [0, 1691, 1692, 1690, 1687, 88, 1688, 1689, 1685, 1757, 1758, 836, 1684, 800, 1686]
        df = df.loc[(df['metric_id'].isin([351, 352, 352])) & (df['attribute_Id'].isin(attr_id))].reset_index(drop=True)
        
        # Appending excel files one by one
        finalexcelsheet = finalexcelsheet.append(df, ignore_index=True)
    # to print the combined data
    print('Final Sheet:')
    # display(finalexcelsheet)
    
    # save combined data
    country = country.capitalize()
    finalexcelsheet.to_excel(f'{country} Main.xlsx',index=False)    


def fetch_country_id(country_name=''):
    url = "https://data.gsmaintelligence.com/api-web/v2/zones_fixed_operator?_limit=500&_sortByFields=name:asc"

    payload = {}
    headers = {
        'authority': 'data.gsmaintelligence.com',
        'accept': '*/*',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'content-type': 'text/plain',
        'cookie': cookie,
        'dnt': '1',
        'referer': 'https://data.gsmaintelligence.com/data/fixed-operator-metrics',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="100", "Google Chrome";v="100"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36'
    }

    # headers = {
    #     'authority': 'data.gsmaintelligence.com',
    #     'accept': '*/*',
    #     'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    #     'cache-control': 'no-cache',
    #     'content-type': 'text/plain',
    #     'cookie': cookie,
    #     'dnt': '1',
    #     'pragma': 'no-cache',
    #     'referer': 'https://data.gsmaintelligence.com/data/fixed-market-metrics',
    #     'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"',
    #     'sec-ch-ua-mobile': '?0',
    #     'sec-ch-ua-platform': '"Windows"',
    #     'sec-fetch-dest': 'empty',
    #     'sec-fetch-mode': 'cors',
    #     'sec-fetch-site': 'same-origin',
    #     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
    # }

    # response = requests.get(
    #     'https://data.gsmaintelligence.com/api-web/v2/zones_fixed_operator?_limit=500&_sortByFields=name:asc',
    #     headers=headers,
    # )  

    response = requests.request("GET", url, headers=headers, data=payload)
    # print(json.loads(response.text)['data'])
    if country_name == '':
        # print([i['name'] for i in json.loads(response.text)['data']])
        return {i['name'].lower(): i['id'] for i in json.loads(response.text)['data']}
    else:
        country_n = country_name.lower()
        return fetch_country_id()[country_n]


def org_id_to_name(country, company=''):
    # zone_id = 612
    zone_id = fetch_country_id(country_name=country)
    url = f"https://data.gsmaintelligence.com/api-web/v2/organisations?type.term=fixed-operator&hasData=true&zone.id={zone_id}&status.id==0,81,85&_sortByFields=name:asc"

    payload = {}

    headers = {
        'authority': 'data.gsmaintelligence.com',
        'accept': '*/*',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'cache-control': 'no-cache',
        'content-type': 'text/plain',
        'cookie': cookie,
        'dnt': '1',
        'pragma': 'no-cache',
        'referer': 'https://data.gsmaintelligence.com/data/fixed-operator-metrics',
        'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
    }

    response = requests.get(
        f'https://data.gsmaintelligence.com/api-web/v2/organisations?type.term=fixed-operator&zone.id={zone_id}&status.id==0,81,85&_sortByFields=name:asc',
        headers=headers,
    )  
    # response = requests.request("GET", url, headers=headers, data=payload)
    if company == '':
        return {i['name']: i['id'] for i in json.loads(response.text)['data']}
    else:
        return org_id_to_name(country, company='')[company]
