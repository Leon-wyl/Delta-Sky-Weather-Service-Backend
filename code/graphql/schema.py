import sys
sys.path.insert(0, "package/")

import os
import json
import boto3
from graphene import ObjectType, Field, String, Int, List, Schema

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
    events: List(Event, )


class Query(ObjectType):
    objects = List(String())

    def resolve_objects(root, info):
        s3 = boto3.client('s3')
        contents = s3.list_objects(Bucket=os.getenv("GLOBAL_S3_NAME"))
        keys = [item['Key'] for item in contents['Contents']]
        return keys

schema = Schema(query=Query)



