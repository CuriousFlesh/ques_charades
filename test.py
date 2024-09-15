import pandas as pd
import numpy as np

# Load your CSV file
df = pd.read_csv('cleaned_movies_updated.csv')

# Replace empty strings and NaN values with 'unknown'
df.replace('', 'unknown', inplace=True)  # Replace empty strings
df.fillna('unknown', inplace=True)       # Replace NaN values

# Replace '[]' in specific columns with 'unknown'
columns_to_check = ['genres', 'cast', 'plot_keywords', 'directors']
for col in columns_to_check:
    df[col] = df[col].replace("[]", 'unknown')

# Replace 0.0 in 'imdb_score' column with NaN
df['imdb_score'] = df['imdb_score'].replace(0.0, np.nan)

# Save the updated DataFrame back to a CSV if needed
df.to_csv('cleaned_movies_updated.csv', index=False)

# Display the updated DataFrame (optional)
print(df.head())
