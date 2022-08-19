import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import sklearn


"""
    Works for MyAnimeList pages recommend using all the pages with genres informations 
    discards all the ones with less then 3 genre type
"""



def get_all_titles(soup):
    result_topics = []
    all_topics = soup.find_all('h2', {'class': 'h2_anime_title'})

    # print(all_topics)
    for topic in all_topics:

        topic = topic.find('a').text

        # topic = str(topic.find('a'))
        # topic = topic.replace('<', '=')
        # topic = topic.replace('>', '=')
        # topic = topic.split('=')
        # topic = topic[int(len(topic)/2)]
        result_topics.append(topic)

    # print(result_topics)
    return result_topics

def get_all_genres(soup):
    result_genre = []
    all_genre = soup.find_all('div', {"class": 'genres js-genre'})
    # print(type(all_genre))
    # print(all_genre)

    for genres in all_genre:
        # print(genres)

        genres = genres.find_all('a')
        # print(genres)
        # print(type(genres))
        in_genre = ''
        count = 0
        for genre in genres:

            # print(genre)
            genre = genre.text
            if in_genre== "":
                in_genre = genre
            else:
                in_genre = in_genre +","+ genre
            count +=1
            if count == 3:
                break
        # print(in_genre)  
            
        result_genre.append(in_genre)

    return result_genre



def post_process(genres):
    post_process_genre = []
    for i in genres:
        i = i.replace('\n', '')
        i = i.replace(' ', '')
        post_process_genre.append(i)
    # print(post_process_genre)
    return post_process_genre


def check_repeated_comma(x):
    list_x = x.split(',')
    if len(list_x) >= 3:
        return x
    else:
        return np.nan


def data_set(url):

    data_set = pd.DataFrame(columns = ["Anime", "Primary_Genre", "Secondary_Genre", "Tertiary_Genre"])

    # Initially get the page from the url and from the content extract all the things properly so page is extracetd
    page = requests.get(url)
    # Soup is created where all the content is parsed as html format so it can be extracted as seen in webpages. 
    soup = BeautifulSoup(page.content, 'html.parser')

    
    title = get_all_titles(soup)
    genres = get_all_genres(soup)
    genres = post_process(genres)

    data_set["Anime"] = pd.Series(title)
    data_set["Primary_Genre"] = pd.Series(genres)
    data_set["Primary_Genre"] = data_set["Primary_Genre"].apply(check_repeated_comma)
    data_set["Secondary_Genre"] = data_set["Secondary_Genre"].fillna('To be filled')
    data_set["Tertiary_Genre"] = data_set["Tertiary_Genre"].fillna('To be filled')

    data_set = data_set.loc[data_set["Primary_Genre"] != np.NaN]
    data_set = data_set.dropna(how = 'any')

    data_set[["Primary_Genre", "Secondary_Genre", "Tertiary_Genre"]] = data_set['Primary_Genre'].str.split(',', expand=True)

    data_set.to_csv('Dataset.csv', mode = 'a', header=False)

    # print(data_set.head())


if __name__ == "__main__":
    import os
    os.system('cls')
    print('MyAnimeList Scraper')


    genre_list = ["1/Action",
                    "2/Adventure",
                    "4/Comedy",
                    "5/Avant_Garde",
                    "7/Mystery",
                    "8/Drama",
                    "10/Fantasy",
                    "14/Horror",
                    "22/Romance",
                    "24/Sci-Fi",
                    "30/Sports",
                    "36/Slice_of_Life",
                    "37/Supernatural",
                    "41/Suspense",
                    "47/Gourmet"
    ]
    
    # number_of_genres  = int(input("Enter number of genres to scrap: "))
    for genre in genre_list:
        # genre = input('Enter a genre: ')
        
        for i in range(1,3):
            url1 = f"https://myanimelist.net/anime/genre/{genre}?page={str(i)}"
            data_set(url1)
            print(f'Scraping page {url1}')
        
