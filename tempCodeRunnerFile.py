# Step 2: Import pandas library
import pandas as pd

# Step 3: Load the CSV file
df = pd.read_csv('cleaned_first_1000_movies.csv')  # Replace with your actual file name

# Step 4: Define a function to count null and 'unknown' values
def count_null_and_unknown(df):
    # Count null (NaN) values
    null_count = df.isnull().sum()
    
    # Count 'unknown' values (case-insensitive)
    unknown_count = (df.applymap(lambda x: str(x).strip().lower()) == 'unknown').sum()
    
    # Combine the two counts
    total_count = null_count + unknown_count
    
    return total_count

# Step 5: Get the frequency of null and 'unknown' values in each column
null_and_unknown_values = count_null_and_unknown(df)

# Step 6: Print the result
print("Frequency of null and 'unknown' values in each column:")
print(null_and_unknown_values)
