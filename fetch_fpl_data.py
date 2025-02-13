import requests
import os
import schedule
import time
from pymongo import MongoClient
from dotenv import load_dotenv


# Load environment variables
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")

# Connect to MongoDB
client = MongoClient(MONGO_URI)
db = client["premier_league"]
collection = db["players"]

# Fetch data from the FPL API
FPL_API_URL = "https://fantasy.premierleague.com/api/bootstrap-static/"

def update_fpl_data():
    """Fetch latest FPL data and update MongoDB efficiently"""
    print("🔄 Fetching latest FPL data...")

    response = requests.get(FPL_API_URL)
    if response.status_code == 200:
        data = response.json()

        # Create mappings for team IDs and position IDs
        team_mapping = {team["id"]: team["name"] for team in data["teams"]}
        position_mapping = {pos["id"]: pos["singular_name"] for pos in data["element_types"]}

        # Process player data
        players = data["elements"]
        for player in players:
            player_data = {
                "name": f"{player['first_name']} {player['second_name']}",
                "team": team_mapping.get(player["team"], "Unknown"),
                "position": position_mapping.get(player["element_type"], "Unknown"),
                "price": player["now_cost"] / 10,
                "total_points": player["total_points"],
                "goals_scored": player["goals_scored"],
                "assists": player["assists"],
                "minutes": player["minutes"]
            }

            # Update existing player data instead of deleting all data
            collection.update_one(
                {"name": player_data["name"]},  # Find by player name
                {"$set": player_data},  # Update existing fields
                upsert=True  # If the player is not in the database, insert them
            )

        print("✅ Successfully updated player data in MongoDB!")
    else:
        print("❌ Failed to fetch FPL data")

