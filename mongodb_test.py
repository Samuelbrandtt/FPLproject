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

# Insert Players if they do not already exist
players = [
    {"name": "M. Salah", "team": "Liverpool", "position": "M", "price": 13.7},
    {"name": "K. De Bruyne", "team": "Man City", "position": "M", "price": 12.5},
    {"name": "E. Haaland", "team": "Man City", "position": "F", "price": 14.0},
    {"name": "B. Saka", "team": "Arsenal", "position": "M", "price": 11.0},
    {"name": "T. Alexander-Arnold", "team": "Liverpool", "position": "D", "price": 8.5},
    {"name": "A. Isak", "team": "Newcastle", "position": "F", "price": 9.5},
    {"name": "M. Ødegaard", "team": "Arsenal", "position": "M", "price": 9.8},
    {"name": "R. James", "team": "Chelsea", "position": "D", "price": 6.0},
]

# Insert only if the player does not already exist
for player in players:
    if not collection.find_one(
        {"name": player["name"]}
    ):  # Check if player already exists
        collection.insert_one(player)
        print(f"Inserted: {player['name']}")
    else:
        print(f"Skipped (already exists): {player['name']}")

# Fetch and print all players from the database
print("\nCurrent players in the database:")
all_players = collection.find()
for player in all_players:
    print(player)

# Find all midfielders
midfielders = collection.find({"position": "M"})

print("\nAll midfielders:")
for player in midfielders:
    print(player)


# Find all players with a price greater than 10
expensive_players = collection.find({"price": {"$gt": 10}})
print("\nAll players with a price greater than 10:")
for player in expensive_players:
    print(player)
