import numpy as np
import tensorflow as tf
import tensorflow_hub as hub
import nltk

import re

import json

# tensroflow hub module for Universal sentence Encoder
module_url = "https://tfhub.dev/google/universal-sentence-encoder-large/3" #@param ["https://tfhub.dev/google/universal-sentence-encoder/2", "https://tfhub.dev/google/universal-sentence-encoder-large/3"]

embed = hub.Module(module_url)

def get_features(texts):
    if type(texts) is str:
        texts = [texts]
    with tf.Session() as sess:
        sess.run([tf.global_variables_initializer(), tf.tables_initializer()])
        return sess.run(embed(texts))
    
def cosineSimilarity(v1, v2):
    mag1 = np.linalg.norm(v1)
    mag2 = np.linalg.norm(v2)
    if (not mag1) or (not mag2):
        return 0
    return np.dot(v1, v2) / (mag1 * mag2)

def semantic_search(query, data, vectors):
#    query = process_text(query)
    print("Extracting features...")
    query_vec = get_features(query)[0].ravel()
    res = []
    for i, d in enumerate(data):
        qvec = vectors[i].ravel()
        sim = cosineSimilarity(query_vec, qvec)
#        sim = cosine_similarity(query_vec, qvec)
        res.append((sim, d[:100], i))
    return sorted(res, key=lambda x : x[0], reverse=True)

