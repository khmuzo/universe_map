import pandas as pd
import plotly.express as px
from pathlib import Path

galaxies = pd.DataFrame({
    "name": ["Milky Way", "Andromeda", "Triangulum"],
    "x": [0, 2.5, 3.0],
    "y": [0, 0.7, -0.4],
    "z": [0, 0.2, 0.1],
    "distance_mly": [0, 2.5, 2.73],
})

fig = px.scatter_3d(
    galaxies,
    x="x",
    y="y",
    z="z",
    hover_name="name",
    hover_data=["distance_mly"],
    title="Tiny 3D Map of Nearby Galaxies"
)

Path("outputs").mkdir(exist_ok=True)

fig.write_html("outputs/universe_map.html")
fig.show()