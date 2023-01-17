from pymongo import MongoClient
def get_database():
 
   # Provide the mongodb atlas url to connect python to mongodb using pymongo
   CONNECTION_STRING = "mongodb+srv://account:bktOHt7GxMg0ETWV@cluster0.owcvdgd.mongodb.net/test"
 
   # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
   client = MongoClient(CONNECTION_STRING)
 
   # Create the database for our example (we will use the same database throughout the tutorial
   return client['plate']

# Get the database
db = get_database()
# Get the collection name
collection_name = "plates"

# Create a new record
def insert_record(record):
    # Get the database
    db = get_database()
    # Insert new record
    db[collection_name].insert_one(record)
    
def insert_many_records(records):
    # Get the database
    db = get_database()
    # Insert new record
    db[collection_name].insert_many(records)

# Get all records
def get_all_records():
    # Get the database
    db = get_database()
    # Get all records
    records = db[collection_name].find({})
    return records

def get_all_records_without_user(tg_id):
    db = get_database()
    records = db[collection_name].find({"tg_id": {"$ne": tg_id}})
    return records

# Get a record with a matching ID
def get_record_with_id(id):
    # Get the database
    db = get_database()
    # Get the record with the id
    record = db[collection_name].find_one({"_id": id})
    return record

# Get a record with a matching name
def get_record(name, value): # name - only string, value - string or int
    # Get the database
    db = get_database()
    # Get the record with the name
    record = db[collection_name].find_one({name: value})
    return record

# Get all records with a matching name
def get_all_user_records(name, value):
    # Get the database
    db = get_database()
    # Get all records
    records = db[collection_name].find({name: value})
    return records

def get_all_user_records_without_user(name, value, tg_id):
    # Get the database
    db = get_database()
    # Get all records
    records = db[collection_name].find({"$and": [{name: value}, {"tg_id": {"$ne": tg_id}}]})
    return records

# Update a record with a matching ID
def update_record(name, value_name, field_name, value):
    # Get the database
    db = get_database()
    # Update the record with the matching id
    db["application"].update_one({name: value_name}, {"$set": {field_name: value}})

def update_record_with_value(field_name, field_value, new_field_name, new_value):
    db = get_database()
    record = db[collection_name].find_one({field_name: field_value})[new_field_name]
    record.append(new_value)
    db[collection_name].update_one({field_name: field_value}, {"$set": {new_field_name: record}})


# Delete a record with a matching ID
def delete_record(name, value):
    # Get the database
    db = get_database()
    # Delete the record with the matching id
    db[collection_name].delete_one({name: value})

# Delete all records
def delete_all_records():
    # Get the database
    db = get_database()
    # Delete all records
    db[collection_name].delete_many({})

# Delete the collection
def delete_collection():
    # Get the database
    db = get_database()
    # Delete the collection
    db.drop_collection(collection_name)

# Delete the database
def delete_database():
    # Get the database
    db = get_database()
    # Delete the database
    db.client.drop_database(db)



  
# This is added so that many files can reuse the function get_database()
if __name__ == "__main__":
    #delete_all_records()
    pass
    
    





    