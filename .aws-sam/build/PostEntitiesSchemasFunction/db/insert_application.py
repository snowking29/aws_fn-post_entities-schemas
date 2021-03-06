import json
import bson
import traceback
import pymongo as py
from time import time
from db_util.get_connection import mongodb_conn
from db_util.get_collection import mongodb_collection
from db_util.get_document import mongodb_document

def application(event):
    start_time = time()
    print("Inicio registro de aplicacion en mongodb")
    body = json.loads(event['body'])
    headers = event['headers']
    
    for header_field, header_field_value in headers.items():
        if (header_field.lower() == "key" and len(header_field_value) != 0):
            key = header_field_value
        if (header_field.lower() == "schematype" and len(header_field_value) != 0):
            schema_type = header_field_value

    conn = mongodb_conn()
    print("Info Base de datos: ", conn.server_info())
    if conn is None:
        #No conexión, salida anticipada
        return

    try:
        collection = conn.schema_service.application
    except py.errors.CollectionInvalid as e:
        traceback.print_exc()
        print("No se encontró la colección en la base de datos: %s" %e)

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