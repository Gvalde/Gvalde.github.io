import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["sales_db"]
companies = mydb["companies"]

def Get_Sales_Data():
    data = []
    _all = companies.find({"status" : "sale"})
    for each in _all:
        data.append(each)
    return data