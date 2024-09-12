import requests
import csv
from bs4 import BeautifulSoup

# Genre mapping
genres_reversed = {
    28: "Action",
    12: "Adventure",
    16: "Animation",
    35: "Comedy",
    80: "Crime",
    99: "Documentary",
    18: "Drama",
    10751: "Family",
    14: "Fantasy",
    36: "History",
    27: "Horror",
    10402: "Music",
    9648: "Mystery",
    10749: "Romance",
    878: "Science Fiction",
    10770: "TV Movie",
    53: "Thriller",
    10752: "War",
    37: "Western"
}

# CSV file path and fieldnames
file_path = 'data.csv'
fieldnames = ['title', 'adult', 'genre', 'id', 'language', 'plot', 'release_date', 'imdb_score', 'imdb_id']


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}

def fetch_genre_from_imdb(imdb_id):
    # Construct the URL for the IMDb movie page
    url = f'https://www.imdb.com/title/{imdb_id}/'

# Send a GET request to fetch the page content
    response = requests.get(url, headers=headers)
    try:
        if response.status_code == 200:  # If the request was successful
            # Parse the HTML content using BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Locate the specific section where genres are listed
            genre_parent = soup.find('div', class_='ipc-chip-list--baseAlt ipc-chip-list ipc-chip-list--nowrap sc-2d37a7c7-4 cZxuoc')  # Adjust this to match the actual parent container
            
            if genre_parent:
                # Find all <span> elements with the class 'ipc-chip__text' within this section
                genre_section = genre_parent.find_all('span', class_='ipc-chip__text')
                
                # Extract the genre names
                genres = [genre.text.strip() for genre in genre_section]
                return genres
            else:
                return []
    except:
        return []



def fetch_movies(api_key, language='en', sort_by='release_date.asc', start_page=1, release_date_gte='1920-01-01'):
    base_url = 'https://api.themoviedb.org/3'
    discover_endpoint = '/discover/movie'
    movie_details_endpoint = '/movie/{movie_id}'
    params = {
        'api_key': api_key,
        'sort_by': sort_by,
        'page': 210,
        'release_date.gte': release_date_gte,
        'with_original_language': language
    }

    with open(file_path, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

        while True:
            response = requests.get(base_url + discover_endpoint, params=params)
            if response.status_code == 200:
                movies = response.json()

                # Extract movie data from the results
                movie_data = []
                for movie in movies['results']:  # Access the list of movies using 'results'
                    mapped_genres = [genres_reversed.get(i, 'Unknown') for i in movie.get('genre_ids', [])]

                    # Fetch detailed movie information, including IMDb ID
                    movie_id = movie.get('id', '')
                    details_response = requests.get(base_url + movie_details_endpoint.format(movie_id=movie_id), params={'api_key': api_key})
                    if details_response.status_code == 200:
                        movie_details = details_response.json()
                        imdb_id = movie_details.get('imdb_id', '')
                    else:
                        imdb_id = ''

                    if not mapped_genres:
                        if imdb_id:
                            imdb_genres = fetch_genre_from_imdb(imdb_id)
                            mapped_genres = imdb_genres
                        else:
                            mapped_genres = ['Unknown22']
                            continue

                    current_movie = {
                        'title': movie.get('title', ''),
                        'adult': movie.get('adult', ''),
                        'genre': ', '.join(mapped_genres),
                        'id': movie.get('id', ''),
                        'language': movie.get('original_language', ''),
                        'plot': movie.get('overview', ''),
                        'release_date': movie.get('release_date', ''),
                        'imdb_score': movie.get('vote_average', ''),
                        'imdb_id': imdb_id
                    }
                    movie_data.append(current_movie)

                # Write all movie data to the CSV file
                writer.writerows(movie_data)

                # Check if there are more pages to fetch
                if params['page'] < movies['total_pages']:
                    print('page done - ',params['page'],movies['total_pages'])
                    params['page'] += 1  # Go to the next page
                else:
                    break  # Stop if there are no more pages
            else:
                print(f"Error: {response.status_code}")
                break


api_key = '333b9d7e46faf8955b5f94ffbc166dde'

# Fetch movies in Hindi
fetch_movies(api_key,language='hi')