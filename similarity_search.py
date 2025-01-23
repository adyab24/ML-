import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.metrics.pairwise import cosine_similarity
from dotenv import load_dotenv
import os

load_dotenv('key.env') #loads environment variables from a file named key.env
csv_path = os.getenv('CSV_PATH')
if csv_path:
    try:
        df = pd.read_csv(csv_path)
        print("CSV loaded successfully!")
    except Exception as e:
        print("Failed to load CSV:", e)
else:
    print("CSV path not found in environment variables.")

#preprocessing
df['short_composition1'] = df['short_composition1'].fillna('')
df['short_composition2'] = df['short_composition2'].fillna('')
df.drop('Is_discontinued',axis=1,inplace=True)
df.drop('type', axis=1,inplace=True)
df.drop('pack_size_label', axis=1, inplace=True)
df['combined_composition'] = df['short_composition1'] + ' ' + df['short_composition2']
df = df.sort_values(by='id', ascending=True)

from sklearn.feature_extraction.text import TfidfVectorizer
tfidf_vectorizer = TfidfVectorizer()
tfidf_matrix = tfidf_vectorizer.fit_transform(df['combined_composition'])

from sklearn.decomposition import TruncatedSVD
svd = TruncatedSVD(n_components=7, n_iter=7, random_state=42)
reduced_matrix = svd.fit_transform(tfidf_matrix)

def calculate_similarity_in_batches(query_index, reduced_matrix, batch_size=1000):
    similarity_scores = []
    for i in range(0, reduced_matrix.shape[0], batch_size):
        batch_end = min(i + batch_size, reduced_matrix.shape[0])
        batch_similarity = cosine_similarity(reduced_matrix[query_index:query_index+1], reduced_matrix[i:batch_end])
        for j in range(batch_similarity.shape[1]):
            similarity_scores.append((i + j, batch_similarity[0, j]))
    similarity_scores.sort(key=lambda x: x[1], reverse=True)
    return similarity_scores

def find_similar_medicines(index, reduced_matrix, top_n):
    similarity_scores = calculate_similarity_in_batches(index, reduced_matrix)
    top_similar_indices = [score[0] for score in similarity_scores[1:top_n + 1]]
    return top_similar_indices

def find_word_in_column(df, column_name, word):
    # Convert both column values and the word to lowercase for case-insensitive search
    df[column_name] = df[column_name].str.lower()
    word = word.lower()
    result = df[column_name].str.contains(word)
    return result

def alternatives(target_index):
    top_n = 5
    similar_medicines_indices = find_similar_medicines(target_index,reduced_matrix,top_n)
    similar_medicines = df.iloc[similar_medicines_indices].to_dict(orient='split')
    # print(f"Top {top_n} similar medicines to {df.loc[target_index, 'name']}:\n")
    # print(similar_medicines[['name', 'price(₹)', 'short_composition1', 'short_composition2']].to_markdown(index=False))
    return similar_medicines

def search_medicine(medicine_found):
    lowercase_column = df['name']
    lowercase_column = lowercase_column.str.lower()
    name=medicine_found.lower()

    if (lowercase_column == name).any():
        index=lowercase_column[lowercase_column == name].index.tolist()
    else:
        index = lowercase_column[lowercase_column.str.contains(name)].index.tolist()

    if index:
        answer=int(index[0])
    else: 
        return (None, None, None, None, None)
    
    med_searched_name=df.loc[answer, 'name']
    comp=df.loc[answer,'combined_composition']
    manu=df.loc[answer,'manufacturer_name']
    price=df.loc[answer,'price(₹)']
    if answer:
        print('Medicine found. Searching for alternatives.')
        similar_meds=alternatives(answer)
    else:
        print("Medicine not found in database")
    return (med_searched_name, comp, similar_meds,manu,price)