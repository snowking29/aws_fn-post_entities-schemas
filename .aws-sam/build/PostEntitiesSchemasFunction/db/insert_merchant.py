import json
import bson
import traceback
import pymongo as py
from time import time
from db_util.get_connection import mongodb_conn
from db_util.get_collection import mongodb_collection
from db_util.get_document import mongodb_document

def merchant(event):
    start_time = time()
    print("Inicio registro de comercio en mongodb")
    body = json.loads(event['body'])
    headers = event['headers']

    for header_field, header_field_value in headers.items():
        if (header_field.lower() == "key" and len(header_field_value) != 0):
            key = header_field_value
            
    print("KEEEEY: ", key)
    conn = mongodb_conn()

    conn = mongodb_conn()
    print("Info Base de datos: ", conn.server_info())
    if conn is None:
        #No conexión, salida anticipada
        return

    try:
        collection = conn.schema_service.merchant
    except py.errors.CollectionInvalid as e:
        traceback.print_exc()
        print("No se encontró la colección en la base de datos: %s" %e)
    
    body.setdefault("key", key)

    result_find_register = mongodb_document(conn,key)
    print("¿Se encontró key?: ", result_find_register)
    
    if result_find_register:
        success = "false"
        code = "01"
        value = "Ya se encuentra un registro para la key enviada."
    else:
        try:
            collection.insert_one(body)
            success = "true"
            code = "00"
            value = "Se registro satisfactoriamente."
        except Exception as e:
            print("Error al insertar documento en base de datos: %s" %e)
    
    
    conn.close() 
    
    response = {
        "success": success,
        "configuration": {
            "meta": {
                "status": {
                    "code": code,
                    "message_ilgn": [{
                        "locale": "es_PE",
                        "value": value
                    }]
                }
                
            }
        }
    }
    print("Response payload: ", json.dumps(response))
    elapsed_time = time() - start_time
    print("Registro Comercio - Tiempo de ejecución ""{:.10f}".format(elapsed_time)," segundos")
    return response