import pandas as pd

df = pd.read_csv('data.csv')

# Convert release_date to datetime, handling errors
df_mod = df.dropna(subset=['release_date'])
df_mod['release_date'] = pd.to_datetime(df_mod['release_date'], errors='coerce')

# Filter out rows with NaT in release_date
df_mod = df_mod.dropna(subset=['release_date'])

# Filter dates
df_filtered = df_mod[df_mod['release_date'] > pd.Timestamp(2024, 9, 1)]

# Remove values in df_mod that are present in df_filtered
df_mod = df_mod[~df_mod.index.isin(df_filtered.index)]
df_mod=df_mod.dropna(subset=['imdb_id','genre'])
