import requests

TMDB_API_KEY = '9456c6fdcf8a04e157e45387ebf0c687'  # Replace with your actual TMDB API key

def get_movie_details(movie_id):
    url = f'https://api.themoviedb.org/3/movie/{movie_id}'
    params = {
        'api_key': TMDB_API_KEY,
        'language': 'en-US',
    }
    response = requests.get(url, params=params)
    return response.json()

