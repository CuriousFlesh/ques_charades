import pandas as pd
import requests

# Load your dataset
df = pd.read_csv('cleaned_first_1000_movies.csv')  # Replace with your actual file name

# Set up your Hugging Face API key and endpoint
API_KEY = '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'  # Replace with your actual Hugging Face API key
API_URL = 'https://api-inference.huggingface.co/models/distilgpt2'

# List of questions to ask
questions = [
    "Is the movie set in a rural village?",
    "Does the plot involve a love story?",
    "Is there a prominent character who is a police officer?",
    "Is the movie based on a true story?",
    "Does the film feature a significant family drama?",
    "Is the main character a woman?",
    "Does the movie have a strong social message?",
    "Is there a supernatural element in the plot?",
    "Does the story involve revenge?",
    "Is the movie known for its music or songs?",
    "Does the plot revolve around a sports event?",
    "Is the film set during a historical period?",
    "Is there a major twist at the end of the movie?",
    "Does the main character travel abroad?",
    "Is the movie part of a popular film franchise?",
    "Is the film primarily in Hindi?",
    "Does the story involve a love triangle?",
    "Is there a character who sacrifices themselves for others?",
    "Is the movie known for its action sequences?",
    "Does the plot include a crime or investigation?",
    "Is the film directed by a well-known filmmaker?",
    "Does the story focus on friendship?",
    "Is there a significant cultural or religious aspect in the film?",
    "Does the main character have a tragic fate?",
    "Is there a comedic element in the movie?",
    "Does the film feature a royal family or historical kings?",
    "Is the plot centered around an educational theme?",
    "Does the movie have a strong antagonist?",
    "Is there a wedding or marriage as a central theme?",
    "Does the movie take place in a metropolitan city?",
]

# Function to ask a question using the LLM via Hugging Face API
def ask_llm(movie, question):
    # Prepare the request payload
    prompt = f"Here are the details of the movie:\n"
    prompt += f"Title: {movie['title']}\n"
    prompt += f"Plot Keywords: {movie['plot_keywords']}\n"
    prompt += f"Genres: {movie['genres']}\n\n"
    prompt += f"Question: {question}\nAnswer:"
    
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json',
    }
    
    data = {
        'inputs': prompt,
        'parameters': {'max_new_tokens': 500},  # Increased max_new_tokens to 100
    }
    
    # Make the API call
    response = requests.post(API_URL, headers=headers, json=data)
    
    # Extract and return the answer
    if response.status_code == 200:
        return response.json()[0]['generated_text'].strip()
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return "Error in response"

# Initialize new columns for the DataFrame
for question in questions:
    df[question] = ""

# Example of usage
for index, movie in df.iterrows():
    print(f"\nMovie: {movie['title']}")
    for question in questions:
        answer = ask_llm(movie, question)
        print(f"{question} {answer}")
        
        # Store the answer in the DataFrame
        df.at[index, question] = answer

# Save the updated DataFrame back to the same CSV file
df.to_csv('cleaned_first_1000_movies.csv', index=False)

print("Questions and answers have been added to 'cleaned_first_1000_movies.csv'.")
