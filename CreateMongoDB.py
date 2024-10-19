from pymongo import MongoClient
import os
import json

mongo_username = os.environ.get('MONGO_USERNAME', 'root') 
mongo_password = os.environ.get('MONGO_PASSWORD', 'example')
# mongo_hostname = os.environ.get('MONGO_HOSTNAME', 'mongodb') 
mongo_hostname = os.environ.get('MONGO_HOSTNAME', 'localhost')
mongo_uri = f"mongodb://{mongo_username}:{mongo_password}@{mongo_hostname}:27017/"

client = MongoClient(mongo_uri)
db = client['coke'] 
read_collection = db['mer_info'] 
write_collection = db['mer_write']

# Path to the directory containing JSON files
json_folder = 'db'

# Iterate over each file in the directory
for filename in os.listdir(json_folder):
    if filename.endswith('.json'):
        file_path = os.path.join(json_folder, filename)
        with open(file_path, 'r') as file:
            # Load JSON data from the file
            json_data = json.load(file)
            # Insert JSON data into the collection
            write_collection.insert_many(json_data)
            print(f"Uploaded data from {filename} to the database.")




