import pyBear.bear as bear
import pymongo

class collection:
    def __init__(self, server, database, collection):
        self.server = server
        self.database = database
        self.collection = collection

        self.connection = pymongo.MongoClient(
            host = bear.server(server).ip, 
            port = bear.server(server).port)
        self.connection[database].authenticate(
            bear.server(server).username, 
            bear.server(server).password, 
            mechanism='SCRAM-SHA-1')


    def list(self):
        return self.connection[self.database].list_collection_names()


    def insert(self, data):
        self.table = self.connection[self.database][self.collection]

        if type(datdda) == dict:
            self.table.insert_one(data)
        elif type(data) == list:
            self.table.insert_many(data)

    def index(self, Column):
        if not self.TableName:
            raise Bear.BadBear('NoTableSelected')

    def change(self, Condition, Value):
        if not self.TableName:
            raise Bear.BadBear('NoTableSelected')
        self.Table = self.Connection[self.DatabasesName][self.TableName]

        Ret = self.Table.update_many(Condition, Value)
        return (Ret.matched_count, Ret.modified_count)

    def Search(self, Condition, Count=None, Sort=None, Limit=None):
        if not self.TableName:
            raise Bear.BadBear('NoTableSelected')
        self.Table = self.Connection[self.DatabasesName][self.TableName]

        if Count:
            Ret = self.Table.find(Condition).count()
            return Ret
        elif Sort and not Limit:
            Ret = self.Table.find(Condition).sort(Sort[0], Sort[1])
        elif Sort and Limit:
            Ret = self.Table.find(Condition).sort(Sort[0], Sort[1]).limit(Limit)
        elif Limit:
            Ret = self.Table.find(Condition).limit(Limit)
        else:
            Ret = self.Table.find(Condition)
            
        return [Item for Item in Ret]

    def drop(self, Condition):
        if not self.TableName:
            raise Bear.BadBear('NoTableSelected')
        self.Table = self.Connection[self.DatabasesName][self.TableName]
            
        return self.Table.delete_many(Condition).deleted_count


    def delete(self):
        return self.connection[self.database][self.collection].drop()


#db.createUser({
# 'user':'Debuger', 
# 'pwd':'A11b22;;', 
# 'roles':[{'role':'readWrite', 'db':'TimeCapsule'}], 
# 'mechanisms':['SCRAM-SHA-1']
# });
