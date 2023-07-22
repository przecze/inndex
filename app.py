import streamlit as st
from sentence_transformers import SentenceTransformer
import numpy as np
import pandas as pd

st.set_page_config(
        page_title='The Inndex',
        layout='wide')

def is_overlapping(span1, span2):
    return not (span1[1] < span2[0] or span1[0] > span2[1])

def prune_results(df):
    df = df.sort_values(by="similarity", ascending=False)

    checked = []
    for _, row in df.iterrows():
        chapter = row['chapter']
        span = row['span']

        if any((row['chapter'] == chapter and is_overlapping(row['span'], span)) for row in checked):
            continue
        else:
            checked.append(row)

        if len(checked) == 10:
            break

    result = pd.DataFrame(checked)
    return result

def get_similarities(query):
    # Load Sentence Transformer Model
    with st.spinner('loading model and obtaining embedding for your query'):
        model = SentenceTransformer('all-MiniLM-L6-v2')

        # Get query embedding
        query_embedding = model.encode(query, normalize_embeddings=True)

        # Delete the model
        del model

    # Load embeddings
    with st.spinner('loading embeddings'):
        emb = np.load('./data/vol1_embeddings.npy')

    with st.spinner('finding best matches'):
        # Compute similarities
        similarities = np.dot(emb, query_embedding)
    del emb

    with st.spinner('retrieving fragments'):
        df = pd.read_pickle('./data/v1_chunks.pickle')
        df['similarity'] = similarities
        df = df.sort_values('similarity', ascending=False)
        df = df.head(10)
    top = prune_results(df)

    return top

def list_results(df):
    for i, row in df.iterrows():
        st.markdown(f"### {row['chapter']}")
        st.markdown(f"**Similarity**: {row['similarity']:.2f}")
        st.markdown(f"{row['fragment']}")
        st.markdown(f"[Read the chapter on wanderinginn.com]({row['url']})")
        st.markdown("---")


st.title('The Inndex')
st.write('Minimal vector-based search engine for The Wandering Inn book series. For now only Volume 1 available')
query = st.text_input("Describe a scene you're looking for")

if query:
    df = get_similarities(query)
    list_results(df)
