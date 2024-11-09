import pandas as pd

# Load the DataFrame
df = pd.read_csv("movies_attr_with_questions.csv")

# Replace "Possible", "Maybe", and "Likely" with "Yes"
df = df.replace({"Possible": "Yes", "Maybe": "Yes", "Likely": "Yes"})

# Drop rows where any column contains the value "no"
df = df[(df != 'no').all(axis=1)]

# Save the modified DataFrame back to the same CSV file
df.to_csv("movies_attr_with_questions.csv", index=False)

# Define a dictionary to store frequencies for each column
unique_value_counts = {col: df[col].value_counts() for col in df.columns}

# Print the frequencies for each column
for col, counts in unique_value_counts.items():
    print(f"Frequencies for column '{col}':")
    print(counts)
    print("\n")
