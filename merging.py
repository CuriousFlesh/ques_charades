import pandas as pd

# Load the DataFrame
df = pd.read_csv("movies_attr_with_questions.csv")

# Define the columns that contain Yes/No attributes (excluding any columns that do not contain such data)
yes_no_columns = [col for col in df.columns if df[col].dtype == 'object']  # Assuming Yes/No columns are of type 'object'

# Filter for movies where all specified columns are 'Yes'
movies_with_no_no_attributes = df[df[yes_no_columns].eq('no').any(axis=1) == False]

# Get the names of the movies
movie_titles = movies_with_no_no_attributes['title']  # Replace 'title' with the actual column name for movie titles if different

# Print the movie titles
print("Movies with no attributes marked as 'No':")
print(movie_titles.shape)
