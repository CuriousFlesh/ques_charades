import requests
import pandas as pd
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor

# Define headers for web requests
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}

# Fetch IMDb movie details (cast, director, movie duration)
def fetch__from_imdb(imdb_id):
    url = f'https://www.imdb.com/title/{imdb_id}/'
    directors = []
    cast = []
    movie_duration = ''
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            # Find movie duration
            time_div = soup.find('div', class_='sc-1f50b7c-0 iPPbjm')
            if time_div:
                time_list = time_div.find('ul', class_="ipc-inline-list ipc-inline-list--show-dividers sc-ec65ba05-2 joVhBE baseAlt")
                time_list_val = time_list.find_all('li', class_='ipc-inline-list__item')
                movie_duration = time_list_val[2].text if len(time_list_val) > 2 else None

            # Find directors and cast
            director_cast = soup.find('div', class_='sc-1f50b7c-2 cpicUu')
            if director_cast:
                dir_list = director_cast.find_all('ul', class_="ipc-inline-list ipc-inline-list--show-dividers ipc-inline-list--inline ipc-metadata-list-item__list-content baseAlt")
                if len(dir_list) > 0:
                    directors = [i.text for i in dir_list[0].find_all('li', class_='ipc-inline-list__item')]
                if len(dir_list) > 1:
                    cast = [i.text for i in dir_list[1].find_all('li', class_='ipc-inline-list__item')]

    except Exception as e:
        print(f"Error fetching data for IMDb ID {imdb_id}: {e}")
    
    return {
        "movie_duration": movie_duration,
        "directors": directors,
        "cast": cast
    }

# Fetch the plot of the movie
def fetch_plot(imdb_id):
    url = f'https://www.imdb.com/title/{imdb_id}/plotsummary/'
    plot = ''
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            plot_list = soup.find('ul', class_='ipc-metadata-list ipc-metadata-list--dividers-between sc-49ddc26b-0 iYPCgk meta-data-list-full ipc-metadata-list--base')
            if plot_list:
                plot = plot_list.find('li').text.strip()
    except Exception as e:
        print(f"Error fetching plot for IMDb ID {imdb_id}: {e}")
    
    return plot

# Update the DataFrame with the fetched data
def update_movie_data(index, row):
    imdb_data = fetch__from_imdb(row['imdb_id'])
    plot = fetch_plot(row['imdb_id']) if pd.isnull(row['plot']) or row['plot'] == '' else row['plot']
    
    return {
        "index": index,
        "cast": imdb_data['cast'],
        "directors": imdb_data['directors'],
        "movie_duration": imdb_data['movie_duration'],
        "plot": plot
    }

# Apply updates in parallel using ThreadPoolExecutor
def update_dataframe_parallel(df):
    updated_data = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(update_movie_data, index, row) for index, row in df.iterrows()]
        for future in futures:
            updated_data.append(future.result())
    
    # Update DataFrame with fetched data
    for data in updated_data:
        index = data['index']
        df.at[index, 'cast'] = data['cast']
        df.at[index, 'directors'] = data['directors']
        df.at[index, 'movie_duration'] = data['movie_duration']
        df.at[index, 'plot'] = data['plot']

# Load the DataFrame
df = pd.read_csv('processed_data.csv')

# Initialize the cast, directors, and movie_duration columns if not present
df['cast'] = None
df['directors'] = None
df['movie_duration'] = None

# Update the DataFrame in parallel
update_dataframe_parallel(df)

df.to_csv('updated.csv',index=False)
