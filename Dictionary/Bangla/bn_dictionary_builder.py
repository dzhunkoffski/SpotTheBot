from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.sparse.linalg import svds
import numpy as np

def make_table_and_dict(corpus_path, min_df, max_df):
    with open(corpus_path, 'r', encoding = 'utf-8') as corpus_file:
        vectorizer = TfidfVectorizer(analyzer = 'word', min_df = min_df, max_df = max_df)
        data_vectorized = vectorizer.fit_transform(corpus_file)
    return data_vectorized, vectorizer.get_feature_names_out(), vectorizer.idf_

def create_table(data_vectorized, k, table_path, name):
    u, sigma, vt = svds(data_vectorized, k)
    # SAVE VECTORS
    with open('bn_data_vectorized.npy', 'wb') as f:
        np.save(f, data_vectorized)
    with open('bn_u_v1.npy', 'wb') as f:
        np.save(f, u)
    with open('bn_sigma_v1.npy', 'wb') as f:
        np.save(f, sigma)
    with open('bn_vt_v1.npy', 'wb') as f:
        np.save(f, vt) 
    # ============
    with open(path + name + str(k) + '.npy', 'wb') as f:
        np.save(f, np.dot(np.diag(sigma), vt).T)

bn_data_vectorized, bn_dictionary, idfs = make_table_and_dict('bn_corpus_cleaned.txt', 0.01, 0.99)
path = ''
with open('bn_words_v1.npy', 'wb') as f:
    np.save(f, bn_dictionary)
print(len(bn_dictionary))
create_table(bn_data_vectorized, 1024, path, "bn_vec_v1_")