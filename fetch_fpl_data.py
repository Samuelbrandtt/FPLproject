import requests
import os
import json
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

# Fetch data from FPL API
response = requests.get(FPL_API_URL)
if response.status_code == 200:
    data = response.json()

    # Create a mapping of team IDs to team names
    teams_data = data["teams"]
    team_mapping = {team["id"]: team["name"] for team in teams_data}

# Create a mapping of position IDs to position names
    position_mapping = {pos["id"]: pos["singular_name"] for pos in data["element_types"]}

    # Extract player data and convert team IDs & position IDs to names
    players = data["elements"]
    formatted_players = []
    for player in players:
        formatted_players.append({
            "name": f"{player['first_name']} {player['second_name']}",
            "team": team_mapping.get(player["team"], "Unknown"),  # Convert index to team name
            "position": position_mapping.get(player["element_type"], "Unknown"),  # Convert index to position
            "price": player["now_cost"] / 10,  # Price is stored as 10x actual value
            "total_points": player["total_points"],
            "goals_scored": player["goals_scored"],
            "assists": player["assists"],
            "minutes": player["minutes"]
        })

    # Clear old data and insert new data
    collection.delete_many({})
    collection.insert_many(formatted_players)

    print("✅ Successfully stored FPL data in MongoDB with correct team names & positions!")
else:
    print("❌ Failed to fetch FPL data")