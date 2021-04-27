import json
import bson
import traceback
from time import time
from get_connection import mongodb_conn
from get_collection import mongodb_collection
from get_document import mongodb_document

def issuer(event):
    start_time = time()
    print("Inicio registro de emisor en mongodb")
    
    body = json.loads(event['body'])
    headers = event['headers']
    key = headers['key']

    conn = mongodb_conn()
    print("Info Base de datos: ", conn.server_info())
    if conn is None:
        #No conexión, salida anticipada
        return
    collection = mongodb_collection(conn,"schema_service","issuer")
    if collection is None:
        #Collection invalido, salida anticipada
        return
    
    body.setdefault("key", key)

    result_find_register = mongodb_document(key)
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
    print("Registro Emisor - Tiempo de ejecución ""{:.10f}".format(elapsed_time)," segundos")
    return response