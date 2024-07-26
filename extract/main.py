 #Instantiate AuthClient object
import base64
from intuitlib.client import AuthClient
from intuitlib.enums import Scopes
import requests
import json               
import pandas as pd, pandas_gbq
import gcsfs
from datetime import datetime


def quickbooksItem(event=None, context=None):
    gcs_file_system = gcsfs.GCSFileSystem(project='focused-studio-351420')
    gcs_json_path = 'gs://quickbooks-refresh-token/quickbooksRefreshToken.json'
    with gcs_file_system.open(gcs_json_path) as f:
      json_dict = json.load(f)    
    
    refresh_token = json_dict['refresh_token']
    
    auth_client = AuthClient(
        client_id='ABtzKlEPa1eHL2wsQp2Scb9626rIarkrdy2wkIy3hH6IYxH3do',
        client_secret='LMSfQ0EuHBSL1Y4SXcgUKwy9sdKJZl6WsfGhsFNl',
        redirect_uri='https://developer.intuit.com/v2/OAuth2Playground/RedirectUrl',
        environment='production')

    auth_client.refresh(refresh_token=refresh_token)

    #Get record count
    url = "https://quickbooks.api.intuit.com/v3/company/9130351877430856/query?query=select count(*) from Item  where active in (true, false)&minorversion=65"

    payload={}
    headers = {
    'User-Agent': 'QBOV3-OAuth2-Postman-Collection',
    'Accept': 'application/json',
    'Authorization': 'Bearer {}'.format(auth_client.access_token)
    }

    countRecords = requests.request("GET", url, headers=headers, data=payload)
    countRecords_ = countRecords.json()
    countRecords_ = countRecords_['QueryResponse']['totalCount']

    #Setting up startposition and maxresult for pagination
    startPosition = list(range(1,int(countRecords_), 1000))
    maxResult = [1000] * len(startPosition)

    #creating list of tuples as input
    urlInput = list(zip(startPosition, maxResult))

    urls = []

    for i, j in urlInput:
        url = "https://quickbooks.api.intuit.com/v3/company/9130351877430856/query?query=select * from Item  where active in (true, false) STARTPOSITION {} MAXRESULTS {}&minorversion=65".format(i,j)
        urls.append(url)
    
    responses = []
    for url in urls:
        url = url
        payload={}
        headers = {
            'User-Agent': 'QBOV3-OAuth2-Postman-Collection',
            'Accept': 'application/json',
            'Authorization': 'Bearer {}'.format(auth_client.access_token)
            }
        response = requests.request("GET", url, headers=headers, data=payload)
        data = json.loads(response.text)
        responses.append(data)
    
    data_ = responses

    list_ = []
    
    for data in data_:
        for i in data["QueryResponse"]["Item"]:
            lst = i
            list_.append(lst)
    
    #Converting list of dictionaries to pandas_df
    df = pd.DataFrame(list_)
    
    # return df
    for col in df.columns.to_list():
        df[col] = df[col].astype("string")

    
    if len(df) == 0:
        pass
    else:
        #Write results to bq table
        destination_table = 'focused-studio-351420.hps_quickbooks.hps_quickbooks_item'
        project_id = 'focused-studio-351420'
        pandas_gbq.to_gbq(df,
                    destination_table,
                    project_id,
                    if_exists='replace',
                    )
        df.to_csv('gs://hps-quickbooks-bigquery-backup/hps_quickbooksItem/hps_quickbooksItem_{}.csv'.format(datetime.now()),index=False)

