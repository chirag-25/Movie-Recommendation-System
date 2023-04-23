
import pandas as pd

import requests
from bs4 import BeautifulSoup
import re



movie_lens_movie_data = pd.read_csv('Movielens dataset/link.csv')
movie_lens_movie_data.head()

movie_lens_movie_data_modified = movie_lens_movie_data[:5].copy()
movie_lens_movie_data_modified
# create column for movie title, summary, score, cast, director, stars, popularity score, number of critic reviews, number of user reviews
new_col = ['summary', 'score', 'cast', 'director', 'stars', 'popularity_score', 'num_critic_reviews', 'num_user_reviews']
movie_lens_movie_data_modified = movie_lens_movie_data_modified.reindex(columns=movie_lens_movie_data_modified.columns.tolist() + new_col)
movie_lens_movie_data_modified

def get_movie_data(movie_id):
    imdb_url = "https://www.imdb.com/title/tt" + str(movie_id).zfill(7) + "/"
    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"}

    # Send a GET request to the URL with headers
    response = requests.get(imdb_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    try:
        
    # total user reviews
        user_reviews_link = soup.find('a', {'class': 'isReview', 'href': lambda x: x and 'reviews' in x})
        num_user_reviews = user_reviews_link.find('span', {'class': 'score'}).text
        movie_lens_movie_data_modified.loc[movie_lens_movie_data_modified['imdbId'] == movie_id, 'num_user_reviews'] = int(num_user_reviews)
    except:
        pass
    
    
    try:
        # num of critic reviews
        critic_reviews_link = soup.find('a', {'class': 'isReview', 'href': lambda x: x and 'externalreviews' in x})
        num_critic_reviews = critic_reviews_link.find('span', {'class': 'score'}).text
        movie_lens_movie_data_modified.loc[movie_lens_movie_data_modified['imdbId'] == movie_id, 'num_critic_reviews'] = int(num_critic_reviews)
        # print(num_critic_reviews)
    except:
        pass
    
    try:
        # popularity score
        popularity_score = soup.find('div', {'class': 'sc-5f7fb5b4-1 bhuIgW'}).text.strip("")
        movie_lens_movie_data_modified.loc[movie_lens_movie_data_modified['imdbId'] == movie_id, 'popularity_score'] = float(popularity_score)
        
    except:
        pass
    
    
    try:
        # ratings
        ratings_score = soup.find('div', {'class': 'sc-bde20123-2 gYgHoj'}).text.strip('').split('/')[0]
        movie_lens_movie_data_modified.loc[movie_lens_movie_data_modified['imdbId'] == movie_id, 'score'] = float(ratings_score)
    except:
        pass
    
    try:
        # Director
        director_name = soup.find('a', {'class': 'ipc-metadata-list-item__list-content-item'}).text
        movie_lens_movie_data_modified.loc[movie_lens_movie_data_modified['imdbId'] == movie_id, 'director'] = director_name
    except:
        pass

    
    
    try:
        # Writers return list
        writers_link = soup.find('a', {'class': 'ipc-metadata-list-item__label--link', 'href': re.compile('fullcredits')})
        writers_container = writers_link.find_next('div', {'class': 'ipc-metadata-list-item__content-container'})
        writers_names = [a.text for a in writers_container.find_all('a', {'class': 'ipc-metadata-list-item__list-content-item'})]
        movie_lens_movie_data_modified.loc[movie_lens_movie_data_modified['imdbId'] == movie_id, 'cast'] = "|".join(writers_names)
    except:
        pass


    try:
        # stars return list
        stars_section = soup.find('a', {'class': 'ipc-metadata-list-item__label--link', 'href': lambda x: x and '/fullcredits/cast' in x}).find_next('div', {'class': 'ipc-metadata-list-item__content-container'})
        stars_links = stars_section.find_all('a', {'class': 'ipc-metadata-list-item__list-content-item--link'})
        stars = [link.text for link in stars_links]
        movie_lens_movie_data_modified.loc[movie_lens_movie_data_modified['imdbId'] == movie_id, 'stars'] = "|".join(stars)
        # print(stars)
    except:
        pass
    
    try:
        # movie information
        movie_info = soup.find('meta', {'name': 'description'})['content']
        movie_lens_movie_data_modified.loc[movie_lens_movie_data_modified['imdbId'] == movie_id, 'summary'] = movie_info
        
    except:
        pass

    # print(f"Num of user reviews: {num_user_reviews}\nNum of critic reviews: {num_critic_reviews}\nPopularity score: {popularity_score}\nRatings: {ratings_score}\nDirector: {director_name}\nWriters: {writers_names}\nStars: {stars}\nMovie info: {movie_info}")
    # movie_lens_movie_data_modified.to_csv('movie_data.csv', index=False)
    
    return None
    
    
if __name__ == "__main__":
    for imdb_id in movie_lens_movie_data_modified['imdbId']:
        print(imdb_id)
        get_movie_data(imdb_id)
        
movie_lens_movie_data_modified.to_csv('movie_data.csv', index=False)   
    
    
    
    