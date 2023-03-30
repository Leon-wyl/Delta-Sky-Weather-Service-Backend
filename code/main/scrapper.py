import sys
sys.path.insert(0, 'package/')

import newrelic.agent
from stations import stations
from stateId import stateId
import requests
import os
import json
import datetime
import boto3
from flagbase import FlagbaseClient, Config, Identity



flagbase = FlagbaseClient(
    config=Config(
        server_key="sdk-server_b68468aa-9ea3-4dae-82a6-68d23ee1f505"
    )
)
user = Identity("all", {})


@newrelic.agent.background_task(name='Create Data Format', group='Data Creation')
def create_new_format():
    return_dict = {}
    return_dict['datasource'] = "Australian Government Bureau of Meteorology"
    return_dict['dataset_type'] = "weather_info"
    return_dict['dataset_id'] = "http://reg.bom.gov.au/fwo/IDN60901/IDN60901.94768.json"
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
    timezone = datetime.datetime.now(datetime.timezone.utc).astimezone().tzname()
    return_dict['time_object'] = {
        "timestamp": now,
        "timezone": timezone,
    }
    return_dict['events'] = []
    return return_dict

@newrelic.agent.background_task(name='Remove Null Entries', group='Data Cleaning')
def get_processed_data(data_dict):
    for object in data_dict['observations']['data']:
        filtered = {k: v for k, v in object.items() if v is not None and v != '-'}
        object.clear()
        object.update(filtered)
    return data_dict

@newrelic.agent.background_task(name='Remove Null Entries', group='Data Cleaning')
def get_state_id(state_code, state_id_list):
    return state_id_list[f"{state_code}"]

@newrelic.agent.web_transaction(name='Retrieve Data from BOM', group='BOM Requests')
def get_weather_data(return_dict):
    state_id_list = {item["State"]: item["ID"] for item in stateId}
    wmo_list = [(station['WMO'], station['State']) for station in stations]

    for wmo in wmo_list:
        id = get_state_id(wmo[1], state_id_list)
        response = requests.get(f"http://reg.bom.gov.au/fwo/{id}60901/{id}60901.{wmo[0]}.json")

        if response.status_code != 200:
            continue
        byte_object = response.content
        data_string = byte_object.decode('utf8').replace("'", '"')
        data_dict = json.loads(data_string)
        data_dict = get_processed_data(data_dict)
        return_dict['events'].append(data_dict['observations']['data'])
    return return_dict

@newrelic.agent.web_transaction(name='Upload to Data Lake', group='Upload Data')
def upload_to_s3(data):
    client = boto3.client('s3')
    dt = datetime.datetime.now()
    ts = int(datetime.datetime.timestamp(dt))
    try:
        bucket = os.getenv("GLOBAL_S3_NAME")
        print('[BUCKET]', bucket)
        client.put_object(
            Bucket=bucket,
            Key=f'F14A_DELTA-{ts}',
            Body=data
        )

        print('SUCESS: uploaded successfully')
        newrelic.agent.record_custom_event('Successful S3 Upload', {'Upload to S3':'Success'}, )
    except Exception as e:
        print('[ERROR] Upload Failed!')
        newrelic.agent.record_custom_event('Failed S3 Upload', {'Upload to S3': e})
        print(e)

@newrelic.agent.lambda_handler()
def scrapper(event, context):
    newrelic.agent.initialize()
    NR_key = "NRAK-7FY4I37ISXM8YMBSMW0WVJKFDGL"
    return_dict = create_new_format()
    return_dict = get_weather_data(return_dict)
    data = json.dumps(return_dict)
    upload_to_s3(data)
    newrelic.agent.shutdown_agent(timeout=10)


if __name__ == "__main__":
    scrapper('hi', 'what')
