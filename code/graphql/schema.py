import datetime
import sys
sys.path.insert(0, 'package/')

if True:
    import os
    import json
    import boto3
    from graphene import ObjectType, Field, String, Int, List, Schema

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
    time_object = Field(EventTimeObject)
    event_type = String()
    attributes = List(AttributeObject)


class Dataset(ObjectType):
    data_source = String()
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
    get_object = String(file=String(default_value="F14A_DELTA"))
    #get_object = Dataset(file=String(default_value="F14A_DELTA"))
    upload_object = Field(String(), key=String(required=True), value=String(required=True))

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
        return json.dumps(obj['Body'].read().decode('utf-8'), default=str)

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
        except Exception as e:
            print('[ERROR] Upload Failed!')
            print(e)
     

schema = Schema(query=Query)