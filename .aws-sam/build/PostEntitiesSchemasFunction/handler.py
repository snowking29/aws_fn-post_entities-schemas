import re
import json
import traceback
from db.insert_acquirer import acquirer
from db.insert_merchant import merchant
from db.insert_application import application
from db.insert_issuer import issuer

def handler(event, context):
    print("Application Event: asdasdsad")
    headers = event['headers']
    
    for header_field, header_field_value in headers.items():
        if (header_field.lower() == "schematype" and len(header_field_value) != 0):
            schema_type = header_field_value
    
    try: 
        if re.search("entity/.*",schema_type):
            schema_allowed_value = re.sub("entity/","",schema_type)
        else:
            schema_allowed_value = "app"
            
        response = eval(schema_allowed_value)(event)
        
    except Exception as e:
        traceback.print_exc()
        response = {"exception",str(e)}
    
    finally:
        return {
            "statusCode": 200,
            "body": json.dumps(response)
        }