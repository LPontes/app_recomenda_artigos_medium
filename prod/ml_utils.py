import pandas as pd
import re
import joblib as jb
from scipy.sparse import hstack, csr_matrix
import numpy as np
import json
import unidecode

mdl_rf = jb.load("random_forest_20210302.pkl.z")
mdl_lgbm = jb.load("lgbm_20210302.pkl.z")
title_vec = jb.load("title_vectorizer_20210302.pkl.z")


def clean_features(data):
    data['title'] = unidecode.unidecode(data['title'])
    data['title'] = data['title'].replace('[^A-Za-z0-9 ]', ' ')
    data['title'] = data['title'].replace(r'[\xa0]', '')
    data['title'] = data['title'].replace(r'\W', ' ')
    data['responses'] = float(data['responses'])
    try:
        data['claps'] = float(data['claps'].replace(r'[Kk]', 'e3'))
    except:
        data['claps'] = 0
    

    return data


def compute_features(data):

    data = clean_features(data)

    features = dict()

    features['claps'] = data['claps']
    features['responses'] = data['responses']

    vectorized_title = title_vec.transform([data['title']])

    num_features = csr_matrix(np.array([features['claps'], features['responses']]))
    feature_array = hstack([num_features, vectorized_title])

    return feature_array


def compute_prediction(data):
    feature_array = compute_features(data)

    if feature_array is None:
        return 0

    p_rf = mdl_rf.predict_proba(feature_array)[0][1]
    p_lgbm = mdl_lgbm.predict_proba(feature_array)[0][1]

    p = 0.5*p_rf + 0.5*p_lgbm
    #log_data(data, feature_array, p)

    return p

def log_data(data, feature_array, p):

    print(data)
    data['prediction'] = p
    data['feature_array'] = feature_array.todense().tolist()
    #print(video_id, json.dumps(data))







