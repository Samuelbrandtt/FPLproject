import os
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
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
players = list(collection.find({}, {"_id": 0}))  # Exlude MongoDB's ObjectID

# Display players in a DataFrame
df = pd.DataFrame(players)

# Streamlit UI
st.title("⚽ FPL Player Database")

# Search Bar for Player Name
search_query = st.text_input("Search for a player (by name):", "")

if search_query:
    df = df[df["name"].str.contains(search_query, case=False, na=False)]

# Use Session State to Store Filters
if "selected_team" not in st.session_state:
    st.session_state.selected_team = "All"

if "selected_position" not in st.session_state:
    st.session_state.selected_position = "All"

# Filter by Team
teams = ["All"] + sorted(df["team"].astype(str).unique().tolist())
st.session_state.selected_team = st.selectbox("Filter by Team", teams, index=0)

# Filter by Position
positions = ["All"] + sorted(df["position"].astype(str).unique().tolist())
st.session_state.selected_position = st.selectbox(
    "Filter by Position", positions, index=0
)

# Apply Filters
filtered_df = df.copy()

if st.session_state.selected_team != "All":
    filtered_df = filtered_df[filtered_df["team"] == st.session_state.selected_team]

if st.session_state.selected_position != "All":
    filtered_df = filtered_df[
        filtered_df["position"] == st.session_state.selected_position
    ]

# Sorting Feature
sort_option = [
    "None",
    "Name (A-Z)",
    "Name (Z_A)",
    "Price (Low to High)",
    "Price (High to Low)",
    "Total Points (High to Low)",
    "Goals Scored (High to Low)",
    "Assists (High to Low)",
    "Minutes Played (High to Low)"
]
sort_by = st.selectbox("Sort Players by", sort_option)

if sort_by == "Name (A-Z)":
    filtered_df = filtered_df.sort_values("name", ascending=True)
elif sort_by == "Name (Z-A)":
    filtered_df = filtered_df.sort_values("name", ascending=False)
elif sort_by == "Price (Low to High)":
    filtered_df = filtered_df.sort_values("price", ascending=True)
elif sort_by == "Price (High to Low)":
    filtered_df = filtered_df.sort_values("price", ascending=False)
elif sort_by == "Total Points (High to Low)":
    filtered_df = filtered_df.sort_values("total_points", ascending=False)
elif sort_by == "Goals Scored (High to Low)":
    filtered_df = filtered_df.sort_values("goals_scored", ascending=False)
elif sort_by == "Assists (High to Low)":
    filtered_df = filtered_df.sort_values("assists", ascending=False)
elif sort_by == "Minutes Played (High to Low)":
    filtered_df = filtered_df.sort_values("minutes", ascending=False)

# Display Filtered Data
st.write("## Players")
st.dataframe(filtered_df[['name', 'team', 'position', 'price', 'total_points', 'goals_scored', 'assists', 'minutes']])

# Visualize Top Scorers
st.write("## Top Goal Scorers")

# Create a bar chart for top goal scorers
top_scorers = filtered_df.sort_values("goals_scored", ascending=False).head(10)

fig, ax = plt.subplots()
sns.barplot(data=top_scorers, x="goals_scored", y="name", ax=ax)
ax.set_xlabel("Goals Scored")
ax.set_ylabel("Player")
ax.set_title("Top Goal Scorers in FPL")

# Display bar chart
st.pyplot(fig)