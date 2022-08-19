import clustering_code
import os

def clean_t_dataset():
    try:
        os.remove('Dataset_to_plot.csv')
    except:
        pass

def get_anime_name():
    input_anime = input("Enter the Anime name: ")
    animes = clustering_code.cluster_everything(input_anime)
    if type(animes) == int:#for return 0
        pass
    else:
        print(animes)

get_anime_name()