import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#loading data
df = pd.read_csv('combined_nyc_park_crime_stats.csv')

sns.set(style="whitegrid")

#determining the number of unique categories
num_categories = df['CATEGORY'].nunique()

#creating a longer palette
palette = sns.color_palette("flare", n_colors=num_categories)

#plotting
plt.figure(figsize=(14, 7))
sns.boxplot(
    data=df,
    x='CATEGORY',
    y='TOTAL',
    palette=palette
)

#log scale
plt.yscale('log')

plt.title('Crime Density by Park Category (All Years)', fontsize=16, fontweight='bold')
plt.xlabel('Park Category', fontsize=12)
plt.ylabel('Total Crime Count (Log Scale)', fontsize=12)

plt.xticks(rotation=30, ha='right', fontsize=10)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()

plt.show()
