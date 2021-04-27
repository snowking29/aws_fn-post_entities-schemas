import json
import bson
import traceback
from time import time
from get_connection import mongodb_conn
from get_collection import mongodb_collection
from get_document import mongodb_document

def application(event):
    start_time = time()
    print("Inicio registro de aplicacion en mongodb")
    body = json.loads(event['body'])
    headers = event['headers']
    key = headers['key']
    schema_type = headers['schemaType']

    conn = mongodb_conn()
    print("Info Base de datos: ", conn.server_info())
    if conn is None:
        #No conexión, salida anticipada
        return
    collection = mongodb_collection(conn,"schema_service","application")
    if collection is None:
        #Collection invalido, salida anticipada
        return

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

    #if schema_type == "application/3ds":
    #    if result_find_register:
    #        brand_code = body['brand_code']
    #        docs_lists = list(collection.find({"general3ds.brand_code":brand_code},{"_id":0}))
    #        if not docs_lists or docs_lists == None:
    #            insert_document = collection.update({"key":key},{"$push": {"general3ds":body}})
    #            success = "true"
    #            code = "00"
    #            value = "Se registro satisfactoriamente."
    #        else:
    #            success = "false"
    #            code = "01"
    #            value = "La marca ya se encuentra registrada."
    #    else:
    #        brand_code = body['brand_code']
    #        docs_brands = list(collection.find({"general3ds.brand_code":brand_code},{"_id":0}))
    #        if not docs_brands or docs_brands == None:
    #            docs_list = []
    #            docs_list.append(body)
    #            payload_3ds = {
    #                "general3ds":docs_list,
    #                "key":key
    #            }
    #            insert_configuration = collection.insert_one(payload_3ds)
    #            success = "true"
    #            code = "00"
    #            value = "Se registro satisfactoriamente."
    #        else:
    #            success = "false"
    #            code = "01"
    #            value = "La marca ya se encuentra registrada."
    #else:
    #    if result_find_register:
    #        success = "false"
    #        code = "01"
    #        value = "Ya se encuentra un registro para la key enviada."
    #    else:
    #        body.setdefault("key", key)
    #        insert_configuration = collection.insert_one(body)
    #        success = "true"
    #        code = "00"
    #        value = "Se registro satisfactoriamente."
    
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
    
    print("Response payload: ",json.dumps(response))
    elapsed_time = time() - start_time
    print("Registro Aplicacion - Tiempo de ejecución ""{:.10f}".format(elapsed_time)," segundos")
    return response