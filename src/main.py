import pandas as pd
import plotly.express as px
import numpy as np
from pathlib import Path

# Ensure outputs folder exists
Path("outputs").mkdir(exist_ok=True)

# Load real data
df = pd.read_csv("data/galaxies.csv")

# Convert degrees → radians
ra_rad = np.deg2rad(df["ra"])
dec_rad = np.deg2rad(df["dec"])
distance = df["distance_mly"]

# Convert spherical → Cartesian coordinates
df["x"] = distance * np.cos(dec_rad) * np.cos(ra_rad)
df["y"] = distance * np.cos(dec_rad) * np.sin(ra_rad)
df["z"] = distance * np.sin(dec_rad)
df["plot_size"] = df["distance_mly"].replace(0, 0.5)

# Make The Milky Way stand out
df["category"] = df["name"].apply(
    lambda name: "You are here" if name == "Milky Way" else "Other galaxies"
)

df.loc[df["name"] == "Milky Way", "plot_size"] = 3

# Plot
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
        "category": True
    },
    size="plot_size",
    # Find the Milk Way Easily
    color="category",
    # Color By Distance Settings
    # color="distance_mly",
    # color_continuous_scale="Viridis",
    size_max=12,
    title="3D Map of Nearby Galaxies"
)

# Make it look like space
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

fig.write_html("outputs/universe_map.html")
fig.show()