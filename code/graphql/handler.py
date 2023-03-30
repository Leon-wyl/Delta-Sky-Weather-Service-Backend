import sys
sys.path.insert(0, 'package/')

import json
import logging
from schema import schema

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)

def handler(event, context):
    headers = event.headers
    query = json.loads(event.body.query)

    # call the schema
    res = schema.execute(query)

    # return the output
    try:
        return {
            "statusCode": 200,
            "body": json.dumps({'keys': keys}),
            "headers": {
                "Content-Type": "application/json",
            },
        }
    except Exception as e:
        LOGGER.error(f"Grpahql api error: {e}")
        return {
            "statusCode": 500,
            "body": json.dumps({'message': "Something went wrong :("}),
            "headers": {
                "Content-Type": "application/json",
            },
        }
