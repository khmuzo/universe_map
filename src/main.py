# -----------------------------
# Imports
# -----------------------------
import pandas as pd
import plotly.express as px
import numpy as np
from pathlib import Path

# -----------------------------
# Setup
# -----------------------------
# Ensure outputs folder exists
Path("outputs").mkdir(exist_ok=True)

def load_data(path):
    return pd.read_csv(path)
# -----------------------------
# Load data
# -----------------------------
# Load galaxy data from CSV
df = load_data("data/galaxies.csv")

# -----------------------------
# Convert RA/DEC to 3D coordinates
# -----------------------------
# Convert degrees to radians because NumPy trig functions expect radians
ra_rad = np.deg2rad(df["ra"])
dec_rad = np.deg2rad(df["dec"])
distance = df["distance_mly"]

# Convert spherical coordinates to Cartesian coordinates
df["x"] = distance * np.cos(dec_rad) * np.cos(ra_rad)
df["y"] = distance * np.cos(dec_rad) * np.sin(ra_rad)
df["z"] = distance * np.sin(dec_rad)

# -----------------------------
# Prepare plotting helpers
# -----------------------------
# Give nearby galaxies a visible marker size
df["plot_size"] = df["distance_mly"].replace(0, 0.5)

# Create a category so the Milky Way can be highlighted separately
df["category"] = df["name"].apply(
    lambda name: "You are here" if name == "Milky Way" else "Other galaxies"
)

# Make the Milky Way easier to see
df.loc[df["name"] == "Milky Way", "plot_size"] = 3

# -----------------------------
# Build 3D plot
# -----------------------------
fig = px.scatter_3d(
    df,
    x="x",
    y="y",
    z="z",
    hover_name="name",
    hover_data={
        "distance_mly": True,
        "x": False,
        "y": False,
        "z": False,
        "plot_size": False,
        "category": True,
    },
    size="plot_size",
    color="category",
    size_max=12,
    title="3D Map of Nearby Galaxies"
)

# Make the plot look more like space
fig.update_layout(
    scene=dict(
        xaxis=dict(showbackground=False),
        yaxis=dict(showbackground=False),
        zaxis=dict(showbackground=False),
    ),
    paper_bgcolor="black",
    plot_bgcolor="black",
    font=dict(color="white")
)

# -----------------------------
# Save and show plot
# -----------------------------
fig.write_html("outputs/universe_map.html")
fig.show()