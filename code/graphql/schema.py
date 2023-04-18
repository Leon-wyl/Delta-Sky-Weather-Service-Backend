import datetime
import sys
sys.path.insert(0, 'package/')

import os
import json
import boto3
from graphene import ObjectType, Field, String, Int, Float, List, Schema, JSONString
import requests

class DatasetTimeObject(ObjectType):
    timestamp = String()
    timezone = String()

class EventTimeObject(ObjectType):
    timestamp = String()
    timezone = String()
    duration = Int()
    duration_unit = String()

class AttributeObject(ObjectType):
    key = String()
    value = String()

class Event(ObjectType):
    sort_order = Int()
    wmo = Int()
    name = String()
    history_product = String()
    local_date_time = String()
    local_date_time_full = String()
    aifstime_utc = String()
    lat = Float()
    lon = Float()
    apparent_t = Float()
    delta_t = Float()
    air_temp = Float()
    dewpt = Float()
    press = Float()
    press_qnh = Float()
    press_msl = Float()
    rain_trace = Float()
    rel_hum = Float()
    wind_dir = Float()
    wind_spd_kmh = Float()
    wind_spd_kt = Float()

class Dataset(ObjectType):
    datasource = String()
    dataset_type = String()
    dataset_id = String()
    time_object = Field(DatasetTimeObject)
    events = List(Event)

class Datafile(ObjectType):
    key = String(required=True)
    contents = String()

    def resolve_contents():
        s3 = boto3.client('s3')
        # obj = s3.get_object(Bucket=os.getenv('GLOBAL_S3_NAME'), key="ANZ_2022-06-01_2023-01-01.json")
        # return obj['Body'].read().decode('utf-8)
        return {"res": "hi"}

class Query(ObjectType):
    all_objects = List(String)
    get_object = Field(Dataset, file=String(default_value="F14A_DELTA"))
    #get_object = Dataset(file=String(default_value="F14A_DELTA"))
    upload_object = Field(String(), key=String(required=True), value=String(required=True))
    weather = Field(String(), state_id=String(), wmo=String())

    def resolve_all_objects(root, info):
        s3 = boto3.client('s3')
        contents = s3.list_objects(Bucket=os.getenv("GLOBAL_S3_NAME"))
        keys = [item['Key'] for item in contents['Contents']]
        print(f"Returning keys {keys}")
        return keys
    
    def resolve_get_object(root, info, file):
        s3 = boto3.client('s3')
        obj = s3.get_object(Bucket=os.getenv('GLOBAL_S3_NAME'), Key=file)
        print("returning dataset")

        data = json.loads(obj['Body'].read())

        print(data)
        return data

    def resolve_upload_object(root, info, key, value):
        client = boto3.client('s3')
        dt = datetime.datetime.now()
        ts = int(datetime.datetime.timestamp(dt))
        try:
            bucket = os.getenv("GLOBAL_S3_NAME")
            print('[BUCKET]', bucket)
            client.put_object(
                Bucket=bucket,
                Key=key,
                Body=value
            )

            print('SUCESS: uploaded successfully')
            return "success"
        except Exception as e:
            print('[ERROR] Upload Failed!')
            print(e)

    def resolve_weather(root, info, state_id, wmo):
        response = requests.get(f"http://reg.bom.gov.au/fwo/{state_id}60901/{state_id}60901.{wmo}.json")
        byte_object = response.content
        return byte_object.decode('utf8').replace("'", '"')

     

schema = Schema(query=Query)