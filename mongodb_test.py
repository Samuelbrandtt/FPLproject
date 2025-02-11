import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")

print("Connecting to MongoDB...")
client = MongoClient(MONGO_URI)

db = client["premier_league"]
collection = db["players"]

# Print all players in the database
print("\nCurrent players in the database:")
all_players = collection.find()
for player in all_players:
    print(player)

# Remove duplicates
pipeline = [
    {"$group": {"_id": "$name", "count": {"$sum": 1}, "ids": {"$push": "$_id"}}},
    {"$match": {"count": {"$gt": 1}}},
]
duplicates = list(collection.aggregate(pipeline))

print("\nRemoving duplicates...")
for player in duplicates:
    player_ids = player["ids"]
    keep_one = player_ids.pop(0)

    # Remove all duplicates
    collection.delete_many({"_id": {"$in": player_ids}})
    print(f"Removed {len(player_ids)} duplicate(s) of player: {player['_id']}")

    print("\nDuplicate removal complete!")

collection.delete_many({"name": {"$in": ["M. Salah", "K. De Bruyne", "E. Haaland", "B. Saka", "T. Alexander-Arnold", "A. Isak", "M. Ødegaard", "R. James"]}})
print("✅ Fake test players removed from MongoDB!")

