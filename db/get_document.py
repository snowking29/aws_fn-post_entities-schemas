import bson
import traceback
import pymongo as py
from connection import mongodb_conn
def mongodb_document(conn,key):
    try:
        db = conn.configuration_service
        all_collections = db.list_collection_names()
        registers = []
        
        for collection in all_collections:
            get_register = db[collection].find({"key":key})
            for register in get_register:
                registers.append(register)
                
        if not registers:
            foundkey = False
        else:
            foundkey = True
        
        return foundkey
    except Exception as e:
        traceback.print_exc()
        print("Error al intentar obtener documento: %s" %e)