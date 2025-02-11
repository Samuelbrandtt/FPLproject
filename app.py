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

# Use Session State to Store Filters
if "selected_team" not in st.session_state:
    st.session_state.selected_team = "All"

if "selected_position" not in st.session_state:
    st.session_state.selected_position = "All"

# Filter by Team
teams = ["All"] + sorted(df["team"].unique().tolist())  # Ensure 'All' is first
st.session_state.selected_team = st.selectbox("Filter by Team", teams, index=0)

# Filter by Position
positions = ["All"] + sorted(df["position"].unique().tolist())  # Ensure 'All' is first
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

# Display Filtered Data
st.write("## Players")
st.dataframe(filtered_df)

# Visualize Player price
st.write("## Player Price Distribution")

# Create a histogram
fig, ax = plt.subplots()
sns.histplot(filtered_df["price"], bins=10, kde=True, ax=ax)
ax.set_xlabel("Price")
ax.set_ylabel("Number of Players")
ax.set_title("Player Price Distribution")

# Display histogram
st.pyplot(fig)

# Visualization Team Speding
st.write("## Team Spending")

# Group by team and sum the price
team_spending = filtered_df.groupby("team")["price"].sum().reset_index()

# Create a bar chart
fig2, ax2 = plt.subplots()
sns.barplot(data=team_spending, x="price", y="team", ax=ax2)
ax2.set_xlabel("Total Team Spending")
ax2.set_ylabel("Team")
ax2.set_title("Team Spending Per Team")

# Display histogram
st.pyplot(fig2)
