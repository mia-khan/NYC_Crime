import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.cm as cm
import matplotlib.colors as mcolors

#loading data
df = pd.read_csv('combined_nyc_park_crime_stats.csv')

#getting top 10 parks
top_parks = df.groupby('PARK')['TOTAL'].sum().sort_values(ascending=False).head(10)

#normalizing for color mapping
normalized = (top_parks - top_parks.min()) / (top_parks.max() - top_parks.min())

colors = sns.color_palette("flare", n_colors=10)
mapped_colors = [colors[int(i * (len(colors)-1))] for i in normalized]

#plotting
sns.set(style="whitegrid")
fig, ax = plt.subplots(figsize=(12, 7))
bars = ax.barh(top_parks.index, top_parks.values, color=mapped_colors)
ax.invert_yaxis()

ax.set_title('Top 10 Most Dangerous Parks (by Total Crime Count)', fontsize=16, fontweight='bold')
ax.set_xlabel('Total Crime Count', fontsize=12)
ax.set_ylabel('Park', fontsize=12)

#creating colormap and colorbar
flare_cmap = mcolors.LinearSegmentedColormap.from_list("flare", colors)
sm = cm.ScalarMappable(cmap=flare_cmap)
sm.set_array(top_parks.values)

cbar = plt.colorbar(sm, orientation='vertical', pad=0.02, ax=ax)
cbar.set_label('Crime Severity (Color Intensity)', fontsize=11)

ax.grid(axis='x', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()
