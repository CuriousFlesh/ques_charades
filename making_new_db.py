import pandas as pd

# Load the cleaned DataFrame
cleaned_df = pd.read_csv('cleaned_first_1000_movies.csv')  # Load the cleaned movies data

# Check for null values in the DataFrame
null_counts = cleaned_df.isnull().sum()

# Print the null counts for each column
print("Null values in each column of cleaned_first_1000_movies:")
print(null_counts[null_counts > 0])  # Only show columns with null values
