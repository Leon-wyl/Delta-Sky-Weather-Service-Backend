import sys
sys.path.insert(0, "package/")

if True:
    import os
    import json
    import boto3
    from graphene import ObjectType, Field, String, Int, List, Schema

s3 = boto3.client('s3')

class DatasetTimeObject(ObjectType):
    timestamp: String()
    timezone: String()

class EventTimeObject(ObjectType):
    timestamp: String()
    timezone: String()
    duration: Int()
    duration_unit: String()

class AttributeObject(ObjectType):
    key: String()
    value: String()

class Event(ObjectType):
    time_object: Field(EventTimeObject)
    event_type: String()
    attributes: List(AttributeObject)


class Dataset(ObjectType):
    data_source: String()
    dataset_type: String()
    dataset_id: String()
    time_object: Field(DatasetTimeObject)
    events: List(Event)

class Datafile(ObjectType):
    key: String()
    contents = String()

    def resolve_contents():
        obj = s3.get_object(Bucket=os.getenv("GLOBAL_S3_NAME"), key="ANZ_2022-06-01_2023-01-01.json")
        return json.loads(obj['Body'].read())

class Query(ObjectType):
    all_objects = List(String)
    objects = List(Datafile)


    # list all objects in the S3 bucket
    def resolve_objects(root, info):
        contents = s3.list_objects(Bucket=os.getenv("GLOBAL_S3_NAME"))
        keys = [item['Key'] for item in contents['Contents']]
        return keys
    
     

schema = Schema(query=Query)



