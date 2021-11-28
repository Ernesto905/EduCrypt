import pymongo

# Replace the uri string with your MongoDB deployment's connection string.
conn_str = "mongodb+srv://Ernesto905:mypassword@cluster0.h8feh.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"

# set a 5-second connection timeout
DBclient = pymongo.MongoClient(conn_str, serverSelectionTimeoutMS=5000)

try:
    print(DBclient.server_info())
except Exception:
    print("Unable to connect to the server.")

db = client.EducryptDatabase
    
collection = db.learningBot



#example code 2 insert
"""
post = {"author": "Mike",
       "text": "My first blog post!",
                  "tags": ["mongodb", "python", "pymongo"]
} 
posts = db.posts
post_id = posts.insert_one(post).inserted_id
post_id
"""
