import pandas as pd

# Load the DataFrame
df = pd.read_csv("movies_attr_with_questions.csv")

# Filter the DataFrame to get the row where title is "Pad Man"
movie_details = df[df['title'] == 'Ra.One']

# Check if the movie is found and print each column with its value
if not movie_details.empty:
    for column, value in movie_details.iloc[0].items():
        print(f"{column}: {value}")
else:
    print("Movie 'Pad Man' not found in the dataset.")
