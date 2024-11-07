import requests
import pandas as pd
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

# Define headers for web requests
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}

# Fetch IMDb movie details (cast only)
def fetch_from_imdb(imdb_id):
    url = f'https://www.imdb.com/title/{imdb_id}/'
    cast = set()  # Using a set to prevent duplicate entries
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            # Find all ul tags with the specified class
            ul_tags = soup.find_all('ul', class_="ipc-metadata-list ipc-metadata-list--dividers-all title-pc-list ipc-metadata-list--baseAlt")
            for ul in ul_tags:
                li_tags = ul.find_all('li')  # Find all <li> tags within each <ul> tag
                for li in li_tags:
                    if "Stars" in li.text or "Star" in li.text:
                        content_container = li.find('div', class_="ipc-metadata-list-item__content-container")
                        if content_container:
                            # Find all items with class ipc-inline-list__item
                            inline_list_items = content_container.find_all('li', class_="ipc-inline-list__item")
                            for item in inline_list_items:
                                cast.add(item.text.strip())  # Use set to avoid duplicates
        else:
            print(f"Failed to retrieve data for IMDb ID {imdb_id} with status code: {response.status_code}")

    except Exception as e:
        print(f"Error fetching data for IMDb ID {imdb_id}: {e}")
    
    return imdb_id, list(cast)  # Return the IMDb ID and cast list

# Load the DataFrame
df = pd.read_csv('data.csv')

# Initialize the new column
df['cast'] = None  

# Use ThreadPoolExecutor for multithreading
with ThreadPoolExecutor(max_workers=10) as executor:  # Adjust the number of workers as needed
    futures = {executor.submit(fetch_from_imdb, row['imdb_id']): index for index, row in df.iterrows()}
    
    # Use tqdm for progress tracking
    for future in tqdm(as_completed(futures), total=len(futures)):
        index = futures[future]  # Get the index for the DataFrame
        try:
            imdb_id, cast = future.result()  # Unpack the result
            df.at[index, 'cast'] = ', '.join(cast) if cast else 'No cast information available'
            if not cast:
                print(f"IMDb ID with no cast information: {imdb_id}")
        except Exception as e:
            print(f"Error processing IMDb ID: {e}")

# Save the updated DataFrame back to the CSV file without altering the existing content
df.to_csv('data.csv', index=False)
