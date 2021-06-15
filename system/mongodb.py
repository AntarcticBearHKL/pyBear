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

        if type(data) == dict:
            self.table.insert_one(data)
        elif type(data) == list:
            self.table.insert_many(data)

    def index(self, column):
        pass

    def change(self, condition, value):
        self.table = self.connection[self.database][self.collection]

        ret = self.table.update_many(condition, value)
        return (ret.matched_count, ret.modified_count)

    def search(self, condition, count=None, sort=None, limitation=None):
        self.table = self.connection[self.database][self.collection]

        if count:
            ret = self.table.find(condition).count()
            return ret
        elif sort and not limitation:
            ret = self.table.find(condition).sort(sort[0], sort[1])
        elif sort and limitation:
            ret = self.table.find(condition).sort(sort[0], sort[1]).limit(limitation)
        elif limitation:
            ret = self.table.find(condition).limit(limitation)
        else:
            ret = self.table.find(condition)
            
        return [item for item in ret]
    def drop(self, Condition):
        if not self.TableName:
            raise Bear.BadBear('NoTableSelected')
        self.Table = self.Connection[self.DatabasesName][self.TableName]
            
        return self.Table.delete_many(Condition).deleted_count


    def delete(self):
        return self.connection[self.database][self.collection].drop()



    def exist(self, name, value):
        if self.search({name, value}, count=Ture):
            return True
        return False

    def existAndChange(self, name, value, newValue):
        if not self.search({name:value}, count=True):
            return False
        self.change({name:value},{'$set':{name:newValue}})
        return True

    def notExistAndInsert(self, name, condition):
        if self.search({name:value}, count=True):
            return False
        self.insert(condition)
        return True

#db.createUser({
# 'user':'Debuger', 
# 'pwd':'A11b22;;', 
# 'roles':[{'role':'readWrite', 'db':'TimeCapsule'}], 
# 'mechanisms':['SCRAM-SHA-1']
# });
