import traceback
import pymongo as py
def mongodb_conn ():
    try:
        return py.MongoClient("mongodb+srv://dbDeveloper:ptOB5jCCCJ8uOaXY@mycluster.4rkjp.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
    except py.errors.ConnectionFailure as e:
        traceback.print_exc()
        print("No fue posible conectarse a la base de datos: %s" %e)