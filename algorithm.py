import pandas as pd

# Load the DataFrame
df = pd.read_csv('movies_attr_with_questions.csv')

# Get a list of all columns except 'title'
question_list = [col for col in df.columns if col != 'title']

def choose_question(questions, rem_df):
    # Initialize variables to track the question with the smallest difference
    best_question = None
    smallest_diff = float('inf')  # Set to a large value initially
    
    for question in questions:
        # Count the 'Yes' and 'No' values for the current question column in rem_df
        value_counts = rem_df[question].value_counts()
        
        # Get the counts for 'Yes' and 'No', default to 0 if not present
        yes_count = value_counts.get('Yes', 0)
        no_count = value_counts.get('No', 0)
        
        # Calculate the absolute difference between 'Yes' and 'No'
        diff = abs(yes_count - no_count)
        
        # If the difference is smaller than the current smallest difference, update
        if diff < smallest_diff:
            smallest_diff = diff
            best_question = question
    
    return best_question

def interactive_filter(df, question_list):
    rem_df = df.copy()  # Start with the full DataFrame
    asked_questions = {}  # Dictionary to store questions and user responses

    while len(rem_df) > 1:
        # Choose the best question based on the current remaining DataFrame
        question = choose_question(question_list, rem_df)
        if not question:
            break  # Exit if no more questions are available

        # Ask the user for their answer
        answer = input(f"{question} (Yes/No): ").strip().capitalize()

        # Normalize answer for flexibility
        if answer.lower() in ["yes", "y"]:
            answer = "Yes"
        elif answer.lower() in ["no", "n"]:
            answer = "No"
        else:
            print("Please answer with 'Yes' or 'No'.")
            continue

        # Store the question and the user's answer
        asked_questions[question] = answer

        # Filter the DataFrame based on the user's answer
        rem_df = rem_df[rem_df[question] == answer]
        
        # If there's only one row left, break out of the loop
        if len(rem_df) <= 1:
            print(rem_df)

        # Remove the asked question from the question list and rem_df to avoid re-asking
        question_list.remove(question)

    # Display the result
    if len(rem_df) == 1:
        print("The movie that matches your answers is:")
        print(rem_df['title'].values[0])
    elif len(rem_df) == 0:
        print("No movies match your answers.")
    else:
        print("Multiple movies match your answers. Here are the titles:")
        print(rem_df['title'].values)

    # Display the dictionary of asked questions and answers
    print("\nQuestions asked and your answers:")
    for q, a in asked_questions.items():
        print(f"{q}: {a}")

# Example usage
interactive_filter(df, question_list)
