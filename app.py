import streamlit as st
from sentence_transformers import SentenceTransformer
import numpy as np
import pandas as pd
from pathlib import Path
import time

import os
import openai
API_KEY = os.environ.get('OPENAI_API_KEY') or Path('./openai_api_key').read_text().strip('\n')

def get_fragment_prototype(user_input):
    # Read from text files
    system_prompt = Path('prompt/system.txt').read_text()
    example_1_input = Path('prompt/example_1_input.txt').read_text()
    example_1_output = Path('prompt/example_1_output.txt').read_text()
    example_2_input = Path('prompt/example_2_input.txt').read_text()
    example_2_output = Path('prompt/example_2_output.txt').read_text()

    conversation = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": example_1_input},
        {"role": "assistant", "content": example_1_output},
        {"role": "user", "content": example_2_input},
        {"role": "assistant", "content": example_2_output},
        {"role": "user", "content": user_input},
    ]

    # Make the API call
    client = openai.OpenAI(api_key=API_KEY)
    start = time.time()
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=conversation
    )
    elapsed = time.time() - start
    return response.choices[0].message.content, elapsed
    

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


if __name__ == '__main__':
    st.title('The Inndex')
    st.write('Minimal vector-based search engine for The Wandering Inn book series. For now only Volume 1 available')
    query = st.text_input("Describe a scene you're looking for")

    if query:
        with st.spinner('Using GPT-3.5-turbo to hallucinate a fragment for embedding similarity search...'):
            fragment, gen_time = get_fragment_prototype(query)
        with st.expander("Hallucinated fragment from GPT-3.5-turbo - used for similarity ranking", expanded=False):
            st.write(fragment)
            st.caption(f"Generated in {gen_time:.2f}s")
        df = get_similarities(fragment)
        list_results(df)
