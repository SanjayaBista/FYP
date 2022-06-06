from ast import Pass
import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


path = Path(r'C:\Users\DeLL\Desktop\aa\rating.csv')
df = pd.read_csv(path)

# pre-processing data
# replacing the null field with the empty string
feature = ['Rating', 'Size', 'Price', 'Description']
for feat in feature:
    df[feat] = df[feat].fillna('')

def merging(row):
    return str(row['Rating'])+" "+str(row['Size'])+" "+str(row['Price'])+" "+str(row['Description'])

df["mergingFeatures"] = df.apply(merging, axis=1)

# Initializing vectorizer class
vector_data = TfidfVectorizer()
# converting string  data into the matrix
matrix_data = vector_data.fit_transform(df["mergingFeatures"])

# retreiving the cosine value of type numpy array and storing in the variable
similarity_score = cosine_similarity(matrix_data)

def getRecommendation(product_id):
    # getting  similar item on the basis of productid from cosine value
    prod_id = df[df.id == product_id]["id"].index.values[0]
    similarJersey = list(enumerate(similarity_score[prod_id]))
    # sorting and reversing the list
    sortedJersey = sorted(similarJersey, key=lambda x: x[1], reverse=True)
    # retreiving the top 4 matched item
    i = 1
    jerseyList = []
    for i in range(1,len(sortedJersey)):
        jersey = sortedJersey[i]
        i += 1
        jerseyList.append(df["id"].iloc[jersey[0]])
        if i > 4:
            return jerseyList
        
def getJerseyID(id):
    try:
        jerseyID = df[df.id == id]["id"].values[0]
    except:
        Pass
    return getRecommendation(product_id=jerseyID)

    
