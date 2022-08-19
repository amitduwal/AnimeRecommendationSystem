
import pre_processing
from sklearn.cluster import KMeans

def Clustered_final_df(df):
    df['Cluster_Id'] = None

    #modify the n_cluster value to tget more detailed clustering
    kmeans = KMeans(n_clusters = 100)
    features = df[['P_Genre', 'S_Genre', 'T_Genre']]
    kmeans.fit(features)
    df['Cluster_Id'] = kmeans.predict(features)
    return df

def cluster_everything(input_anime):
    df = pre_processing.pre_process_all()
    
    df = Clustered_final_df(df)
  
    df.to_csv('Dataset_to_plot.csv')
    #check if the anime is present or not
    input_anime = input_anime.lower()
    try:
        anime_not_found = df.loc[~df['Anime'].str.contains(input_anime)]
        if len(anime_not_found) == 0:
            print('Anime not found')
            return 0
        get_cluster = df['Cluster_Id'].loc[df['Anime'].str.contains(input_anime)].values[0]
        similar_animes_list = df['Anime'].loc[df['Cluster_Id'] == get_cluster].values
        return similar_animes_list
    except:
        print('Anime not found')
        return 0

#test
cluster_everything('Tokyo Ghoul')