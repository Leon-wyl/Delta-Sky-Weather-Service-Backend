from datetime import datetime


def handler(event, context):
    print("Scheduled function is called")
    print("Time now is", datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
    print("event", event)
    print("context", context)
