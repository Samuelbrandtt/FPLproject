import os
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")

# Connect to MongoDB
client = MongoClient(MONGO_URI)
db = client["premier_league"]
collection = db["players"]

# Fetch players from MongoDB
players = list(collection.find({}, {"_id": 0}))  # Exclude MongoDB's ObjectID

# Display players in a DataFrame
df = pd.DataFrame(players)

# Streamlit UI
st.title("⚽ FPL Player Database")

# Layout: Five columns for filters/search and tables
col1, col2, col3, col4, col5 = st.columns([2, 3, 2, 2, 2])  # First for filters/search, the rest for tables

# Left column: Filters and Search
with col1:
    # Search Bar for Player Name
    search_query = st.text_input("🔍 Search for a player:", "")

    if search_query:
        df = df[df["name"].str.contains(search_query, case=False, na=False)]

    # Use Session State to Store Filters
    if "selected_team" not in st.session_state:
        st.session_state.selected_team = "All"

    if "selected_position" not in st.session_state:
        st.session_state.selected_position = "All"

    # Filter by Team
    teams = ["All"] + sorted(df["team"].astype(str).unique().tolist())
    st.session_state.selected_team = st.selectbox("🏆 Filter by Team", teams, index=0)

    # Filter by Position
    positions = ["All"] + sorted(df["position"].astype(str).unique().tolist())
    st.session_state.selected_position = st.selectbox("🎯 Filter by Position", positions, index=0)

    # Apply Filters (without Sorting)
    filtered_df = df.copy()

    if st.session_state.selected_team != "All":
        filtered_df = filtered_df[filtered_df["team"] == st.session_state.selected_team]
    if st.session_state.selected_position != "All":
        filtered_df = filtered_df[filtered_df["position"] == st.session_state.selected_position]

# Column 2: Display the Players table (Make sure it's larger now)
with col2:
    st.write("## 🏅 Players")
    st.dataframe(filtered_df[['name', 'team', 'position', 'price', 'total_points', 'goals_scored', 'assists', 'minutes']], width=1000, use_container_width=True)

# Column 3: Top Goal Scorers (Apply position filter)
with col3:
    # Filter the Top Goal Scorers table based on selected position
    top_scorers = filtered_df.nlargest(5, "goals_scored")
    st.write("### ⚽ Top Goal Scorers")
    st.dataframe(top_scorers[['name', 'goals_scored']], width=500, use_container_width=True)

# Column 4: Top Assist Providers (Apply position filter)
with col4:
    # Filter the Top Assist Providers table based on selected position
    top_assists = filtered_df.nlargest(5, "assists")
    st.write("### 🅰️ Top Assist Providers")
    st.dataframe(top_assists[['name', 'assists']], width=500, use_container_width=True)

# Column 5: Most Minutes Played (Apply position filter)
with col5:
    # Filter the Most Minutes Played table based on selected position
    most_minutes = filtered_df.nlargest(5, "minutes")
    st.write("### ⏳ Most Minutes Played")
    st.dataframe(most_minutes[['name', 'minutes']], width=500, use_container_width=True)