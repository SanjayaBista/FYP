import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


path = Path(r'C:\Users\DeLL\Desktop\aa\rating.csv')
df = pd.read_csv(path)

# pre-processing data
# replacing the null field with the empty string
features = ['Rating', 'Size', 'Price', 'Description']
for feature in features:
    df[feature] = df[feature].fillna('')

# merging all the fields


def combined_feature(row):
    return str(row['Rating'])+" "+str(row['Size'])+" "+str(row['Price'])+" "+str(row['Description'])


df["merged_feature"] = df.apply(combined_feature, axis=1)

# Initializing vectorizer class
vector_data = TfidfVectorizer()
# converting string of data into the matrix
matrix_data = vector_data.fit_transform(df["merged_feature"])

# retreiving the cosine value of type numpy array and storing in the variable
similarity_score = cosine_similarity(matrix_data)


def get_recommended_room(product_id):
    # getting list of similar room on the basis of room_id from cosine value
    r_id = df[df.id == product_id]["id"].index.values[0]
    similar_room = list(enumerate(similarity_score[r_id]))
    # sorting and reversing the list
    sorted_room = sorted(similar_room, key=lambda x: x[1], reverse=True)
    # retreiving the top 10 matched item
    i = 1
    room_list = []
    for i in range(1,len(sorted_room)):
        room = sorted_room[i]
        i += 1
        room_list.append(df["id"].iloc[room[0]])
        if i > 3:
            return room_list
        


def get_room_from_id(id):
    
    try:
        room_ids = df[df.id == id]["id"].values[0]
    except:
        message = str(id) + " id Room is not avaiable"
        return message
    return get_recommended_room(product_id=room_ids)

    
