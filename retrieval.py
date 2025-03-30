from helpers import data_to_vec, cosine_similarity
from dataset import DATASET

def retrieve(query, top_n=5, similarity_function=cosine_similarity):
    query_embedding = data_to_vec(query)
    dataset = []
    for key, data in DATASET.items():
        for line in data:
            similarity = similarity_function(query_embedding, line["vector"])
            dataset.append((key, similarity, line["original"]))
    return sorted(dataset, key=lambda x: x[1], reverse=True)[:top_n]