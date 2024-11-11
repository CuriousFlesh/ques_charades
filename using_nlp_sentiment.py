import pandas as pd
import spacy
from multiprocessing import Pool, cpu_count
from tqdm import tqdm

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Tone mapping dictionaries
genre_tone_mapping = {
    'action': ['tense', 'dark', 'exciting'],
    'comedy': ['lighthearted', 'funny', 'uplifting'],
    'drama': ['emotional', 'serious', 'thought-provoking'],
    'horror': ['dark', 'scary', 'intense'],
    'romance': ['uplifting', 'heartwarming'],
    'sci-fi': ['futuristic', 'thought-provoking', 'tense'],
    'thriller': ['suspenseful', 'dark', 'tense']
}

keyword_tone_mapping = {
    'war': 'dark',
    'love': 'uplifting',
    'battle': 'intense',
    'future': 'futuristic',
    'alien': 'futuristic',
    'journey': 'adventurous',
    'revenge': 'tense',
    'crime': 'suspenseful',
    'family': 'heartwarming',
    'comedy': 'funny',
    'monster': 'scary',
    'mystery': 'suspenseful'
}

# Function to filter out stopwords and refine keywords
def extract_keywords(plot):
    if pd.isnull(plot):
        return []
    
    doc = nlp(plot)
    keywords = set()

    # Extract named entities
    for ent in doc.ents:
        if not ent.text.lower() in nlp.Defaults.stop_words:
            keywords.add(ent.text.lower())

    # Extract nouns, adjectives, and verbs
    for token in doc:
        if token.pos_ in ['NOUN', 'PROPN', 'ADJ', 'VERB'] and not token.is_stop and len(token.text) > 2:
            keywords.add(token.text.lower())

    return list(keywords)

# Function to determine tone of the movie
def determine_tone(keywords, genres):
    # Initialize an empty set to avoid duplicate tones
    combined_tones = set()

    # Get tones for each genre in the list
    for genre in genres:
        genre_tones = genre_tone_mapping.get(genre.lower(), ['neutral'])
        combined_tones.update(genre_tones)

    # Get tones from the keyword mapping
    keyword_tones = [keyword_tone_mapping.get(kw, 'neutral') for kw in keywords]
    combined_tones.update(keyword_tones)

    # Limit the number of tones to 3 and return them
    return list(combined_tones)[:3]  # Restrict to max 3 tones

# Function to process a chunk of data and extract refined keywords
def process_chunk(chunk):
    # Extract refined keywords from the plot
    chunk['plot_keywords'] = chunk['plot'].apply(extract_keywords)
    
    # Ensure genres is a list by splitting on commas
    chunk['genres'] = chunk['genre'].apply(lambda x: x.split(', ') if isinstance(x, str) else [])
    
    # Determine the tone based on keywords and genres
    chunk['movie_tone'] = chunk.apply(lambda row: determine_tone(row['plot_keywords'], row['genres']), axis=1)
    
    return chunk

# Process data in chunks for large CSV file
def process_data_in_chunks(file_path, chunk_size=1000):
    # Read the CSV file in chunks
    chunks = pd.read_csv(file_path, chunksize=chunk_size)
    
    # Create an empty DataFrame to store results
    results = pd.DataFrame()

    for chunk in tqdm(chunks):
        chunk = process_chunk(chunk)
        results = pd.concat([results, chunk], ignore_index=True)
        print(results['movie_tone'])
        print(results['plot_keywords'])
    
    return results

# Define the file path and process the data
file_path = 'updated.csv'
processed_data = process_data_in_chunks(file_path)

# Save the processed data with refined keywords and tones
processed_data.to_csv('processed_movies_data_with_refined_keywords.csv', index=False)
