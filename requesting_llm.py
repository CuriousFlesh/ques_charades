import google.generativeai as genai
import os

genai.configure(api_key='AIzaSyB8mL8iJoNr1tKpANIWlkE47ssv4z8kE-w') 
import pandas as pd
import time
import concurrent.futures

# Load the dataset
df = pd.read_csv('new_data.csv')

# Reformulated questions
questions_reformulated = [
    "Is the movie primarily a love story or romance?",
    "Does the plot revolve around family dynamics or drama?",
    "Is there a significant element of friendship in the movie?",
    "Is the movie set in a rural village?",
    "Is there a major focus on social or political issues?",
    "Does the movie feature a strong female lead character?",
    "Is the protagonist seeking revenge as part of the story?",
    "Is there a supernatural or fantasy element in the plot?",
    "Is the movie set during a historical period?",
    "Does the plot involve a wedding or marriage as a central theme?",
    "Is there a significant action or crime-related element in the movie?",
    "Is the movie a biopic or based on true events?",
    "Does the film involve a journey or travel as part of the story?",
    "Is the movie known for its music or significant song sequences?",
    "Does the movie take place in a metropolitan city or urban setting?"
]

# Instantiate the Gemini model
model = genai.GenerativeModel("gemini-1.5-flash")

# Function to generate responses for a single movie
def ask_movie_questions_single_request(movie):
    title = movie['title']
    genre = movie['genre']
    plot = movie['plot']

    # Combine all questions into a single prompt
    prompt = (
        f"Movie Title: {title}\n"
        f"Genre: {genre}\n"
        f"Plot: {plot}\n\n"
        "Please answer the following yes/no questions in the format:\n"
        "1. **Answer** (Explanation)\n"
        "2. **Answer** (Explanation)\n"
        "...\n\n"
        "Answer the following yes/no questions. If the answer cannot be determined, say 'no':\n\n"
    )
    prompt += "\n".join([f"{idx + 1}. {question}" for idx, question in enumerate(questions_reformulated)])

    # Send the single request
    try:
        response = model.generate_content(prompt)
        answers = []
        if response and response.candidates:
            response_text = response.candidates[0].content.parts[0].text.strip()
            for line in response_text.split("\n"):
                if line.strip():
                    if len(line.split("**")[0]) > 5:
                        continue
                    answer = line.split("**")[1].strip()
                    if answer == 'Possibly':
                        answer = 'Yes'
                    answers.append(answer)
            while len(answers) < len(questions_reformulated):
                answers.append('no')
        else:
            answers = ['no'] * len(questions_reformulated)
    except Exception as e:
        print(f"Error occurred while generating response for '{title}': {e}")
        answers = ['no'] * len(questions_reformulated)

    # Return the movie data with responses
    return pd.DataFrame([{'Title': title, 'Genre': genre, 'Plot': plot, **dict(zip(questions_reformulated, answers))}])

# Create a new DataFrame to hold the results
results_df = pd.DataFrame(columns=['Title', 'Genre', 'Plot'] + questions_reformulated)

# Function to process each movie with a delay between calls
def process_movie_with_delay(index):
    movie = df.iloc[index]
    movie_data = ask_movie_questions_single_request(movie)
    time.sleep(6)  # Wait 6 seconds after each request
    return movie_data

# Use ThreadPoolExecutor to handle requests concurrently
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    futures = [executor.submit(process_movie_with_delay, i) for i in range(len(df))]
    for future in concurrent.futures.as_completed(futures):
        try:
            # Append each result as it completes
            movie_data = future.result()
            results_df = pd.concat([results_df, movie_data], ignore_index=True)
        except Exception as e:
            print(f"An error occurred: {e}")

# Save the results to a CSV file
results_df.to_csv('movies_with_llm_responses_full.csv', index=False)
print("Updated CSV file saved as 'movies_with_llm_responses_full.csv'")
