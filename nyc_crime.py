import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def read_all_sheets_from_excel(filepath):
    """Read all sheets from an Excel file into a dictionary of dataframes"""
    xl = pd.ExcelFile(filepath)
    return {sheet_name: xl.parse(sheet_name) for sheet_name in xl.sheet_names}

filepaths = {
    '2024_Q1': 'nyc-park-crime-stats-q1-2024.xlsx',
    '2024_Q2': 'nyc-park-crime-stats-q2-2024.xlsx',
    '2024_Q3': 'nyc-park-crime-stats-q3-2024.xlsx',
    '2024_Q4': 'nyc-park-crime-stats-q4-2024.xlsx',
    '2023_Q1': 'nyc-park-crime-stats-q1-2023.xlsx',
    '2023_Q2': 'nyc-park-crime-stats-q2-2023.xlsx',
    '2023_Q3': 'nyc-park-crime-stats-q3-2023.xlsx',
    '2023_Q4': 'nyc-park-crime-stats-q4-2023.xlsx'
}

list_of_dfs = []

for key, fp in filepaths.items():
    try:
        all_sheets = read_all_sheets_from_excel(fp)
        sheet_name = list(all_sheets.keys())[0]
        df = all_sheets[sheet_name]

        df = df.iloc[2:].reset_index(drop=True)  # Remove the first two rows
        df.columns = df.iloc[0]  # Set the header row
        df = df.iloc[1:].reset_index(drop=True)  # Remove the header row from data

        df['quarter'] = key
        list_of_dfs.append(df)
        print('Loaded and cleaned file: ' + fp + ' as ' + key)
        print("Cleaned DataFrame Head:")
        print(df.head())
    except Exception as e:
        print('Error loading file: ' + fp + ' with error ' + str(e))

combined_df = pd.concat(list_of_dfs, ignore_index=True)

combined_df.columns = [col.strip() for col in combined_df.columns]

numeric_columns = ['SIZE (ACRES)', 'MURDER', 'RAPE', 'ROBBERY', 'FELONY ASSAULT',
                   'BURGLARY', 'GRAND LARCENY', 'GRAND LARCENY OF MOTOR VEHICLE', 'TOTAL']
for col in numeric_columns:
    if col in combined_df.columns:
        combined_df[col] = pd.to_numeric(combined_df[col], errors='coerce').fillna(0)

print('Combined DataFrame head:')
print(combined_df.head())

# Visualization 1: Bar chart showing crime distribution by borough
crime_by_borough = combined_df.groupby('BOROUGH')['TOTAL'].sum().reset_index()

plt.figure(figsize=(12, 6))
bar_plot = sns.barplot(data=crime_by_borough, x='BOROUGH', y='TOTAL', palette='viridis')
plt.title('Crime Distribution by Borough')
plt.xlabel('Borough')
plt.ylabel('Total Crime Count')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('crime_distribution_barchart.png')
plt.show()

# Visualization 2: Stacked bar chart that compares different crime types by borough
crime_types = ['MURDER', 'RAPE', 'ROBBERY', 'FELONY ASSAULT', 'BURGLARY', 'GRAND LARCENY',
               'GRAND LARCENY OF MOTOR VEHICLE']
crime_by_type = combined_df.groupby('BOROUGH')[crime_types].sum()

plt.figure(figsize=(12, 6))
crime_by_type.plot(kind='bar', stacked=True, figsize=(12, 6), colormap='tab20')
plt.title('Crime Types by Borough')
plt.xlabel('Borough')
plt.ylabel('Number of Crimes')
plt.legend(title='Crime Type', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.savefig('crime_types_stacked.png')
plt.show()


# Visualization 3: Scatter plot analyzing relationship between park size and crime count
plt.figure(figsize=(12, 6))
scatter_plot = sns.scatterplot(data=combined_df, x='SIZE (ACRES)', y='TOTAL', hue='BOROUGH', palette='deep')
plt.title('Relationship Between Park Size and Crime Count')
plt.xlabel('Park Size (Acres)')
plt.ylabel('Total Crime Count')
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.savefig('parksize_vs_crime.png')
plt.show()
