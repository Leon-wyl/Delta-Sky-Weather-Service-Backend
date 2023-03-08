import sys
sys.path.insert(0, 'package/')

import requests
import json
import datetime

def create_new_format(data_dict):
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
    events_list = []
    for item in data_dict['observations']['data']:
        event_object = {}
        event_object['time_object'] = {
            "timestamp": now,
            "duration": 1,
            "duration_unit": "second",
            "timezone": timezone,
        }
        event_object['event_type'] = "weather data"
        event_object['attribute'] = item
        events_list.append(item)
    return_dict['events'] = events_list
    return return_dict

def get_processed_data(data_dict):
    for object in data_dict['observations']['data']:
        filtered = {k: v for k, v in object.items() if v is not None and v != '-'}
        object.clear()
        object.update(filtered)
    return data_dict
    
def scrapper():
    response = requests.get('http://reg.bom.gov.au/fwo/IDN60901/IDN60901.94768.json')
    bytes = response.content
    data_string = bytes.decode('utf8').replace("'", '"')
    data_dict = json.loads(data_string)
    data_dict = get_processed_data(data_dict)
    data_dict = create_new_format(data_dict)
    data_dict = json.dumps(data_dict)
    print(data_dict)

if __name__ == "__main__":
    scrapper()
