from flask import Flask
from flask_caching import Cache
import pymongo
import os

# Initialize Flask app
app = Flask(__name__)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

# Initialize Cache
# Cache is currently unused within the app
config = {
    "CACHE_TYPE": "SimpleCache",  # Flask-Caching related configs
    "CACHE_DEFAULT_TIMEOUT": 300
}
app.config.from_mapping(config)
cache = Cache(app)

# Connect to database
try:
    mongo = pymongo.MongoClient(
        host="localhost",
        port=27017,
        serverSelectionTimeoutMS = 1000
    )
    db = mongo.inventory
    mongo.server_info()
except:
    print("Could not connect to database")

# Import here to prevent circular imports
from flaskinventory import routes