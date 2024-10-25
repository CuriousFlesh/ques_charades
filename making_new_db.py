import pandas as pd

# Load the dataset
df2 = pd.read_csv("new_data.csv")

# Function to count words in a given text
def count_words(text):
    if isinstance(text, str):  # Ensure the text is a string
        return len(text.split())
    return 0  # Return 0 for non-string entries

# Apply the function to the 'plot' column to get the word counts
df2['word_count'] = df2['plot'].apply(count_words)

# Filter for plots with fewer than 10 words
less_than_10_words = df2[df2['word_count'] < 15]

# Print the titles and corresponding plots
for index, row in less_than_10_words.iterrows():
    print(f"Movie: {row['title']}, Plot: {row['plot']}")
