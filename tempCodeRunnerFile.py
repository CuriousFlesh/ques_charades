import pandas as pd

# Load the DataFrame
df = pd.read_csv("data.csv")
df2=pd.read_csv("movies_attr_with_questions.csv")
# Define the lists of directors for each question
directors_dict = {
    "Is the movie directed by David Dhawan, Mahesh Bhatt, Ram Gopal Varma, Vikram Bhatt, or Priyadarshan?": [
        "David Dhawan", "Mahesh Bhatt", "Ram Gopal Varma", "Vikram Bhatt", "Priyadarshan"
    ],
    "Is the movie directed by Rama Rao Tatineni, K. Bapaiah, Ram Gopal Varma, Vikram Bhatt, or David Dhawan?": [
        "Rama Rao Tatineni", "K. Bapaiah", "Ram Gopal Varma", "Vikram Bhatt", "David Dhawan"
    ],
    "Is the movie directed by Shantaram Rajaram Vankudre, Mehboob Khan, Hrishikesh Mukherjee, Bimal Roy, or Adoor Gopalakrishnan?": [
        "Shantaram Rajaram Vankudre", "Mehboob Khan", "Hrishikesh Mukherjee", "Bimal Roy", "Adoor Gopalakrishnan"
    ]
}

# Function to check if the movie is directed by any of the specified directors
def check_directors(director_list, row):
    directors = eval(row['directors'])  # Convert string representation of the list to a Python list
    return 'Yes' if any(director in directors for director in director_list) else 'No'

# Apply checks for each question and store results in new columns
for question, director_list in directors_dict.items():
    df[question] = df.apply(lambda row: check_directors(director_list, row), axis=1)

# Count Yes and No for each question
for question in directors_dict.keys():
    counts = df[question].value_counts()
    print(f"Counts for '{question}':")
    print(counts)
    print()  # Print a new line for better readability
print(df.columns)
# Optionally save the updated DataFrame to a new CSV file
#df.to_csv('movies_attr_with_director_checks.csv', index=False)
