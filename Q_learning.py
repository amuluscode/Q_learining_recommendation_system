import streamlit as st
import pandas as pd
import numpy as np
import random




items_df = pd.read_csv('items.csv')

num_items = len(items_df)

#parameters
alpha, gamma, epsilon = 0.2,0.9, 0.6

if "q_values" not in st.session_state:
    st.session_state.q_values = np.zeros(num_items)

if "recommendations" not in st.session_state:
    st.session_state.recommendations = random.sample(range(num_items),10)


def item_similarity(item1, item2):
    score = 0

    if item1['category'] == item2['category']:
        score += 1

    if item1['brand'] == item2['brand']:
        score += 1

    return score

def update_q(clicked_item_id, reward = 1):

    st.session_state.q_values[clicked_item_id] += alpha * (reward - st.session_state.q_values[clicked_item_id])

    clicked_item = items_df.iloc[clicked_item_id]

    for i in range(num_items):
        if i!= clicked_item_id:
            sim = item_similarity(clicked_item, items_df.iloc[i])

            if sim > 0:
                st.session_state.q_values[i] += alpha * (0.5 * reward * sim - st.session_state.q_values[i])



def recommend_next_top10():
    if np.random.rand() < epsilon:
        return random.sample(range(num_items), 10)
    
    q_vals = st.session_state.q_values
    top_indices = np.argsort(q_vals)[-10:][::-1]  # Fixed line
    return list(top_indices)

#ui
st.title("Ecommerce Recommender for you:")

st.write("### Recommended for you:")

recommendations = st.session_state.recommendations

cols_per_row = 4

rows = (len(recommendations) + cols_per_row - 1) // cols_per_row

for row_idx in range(rows):
        cols=st.columns(cols_per_row)
        for col_idx,item_idx in enumerate(range(row_idx * cols_per_row, (row_idx + 1) * cols_per_row)):

            if  item_idx >=len(recommendations):
                break

            item_id=recommendations[item_idx]
            item=items_df.iloc[item_id]

            with cols[col_idx]:
                st.markdown(f"**{item['name']}**")
                st.markdown(f"Category: {item['category']}")
                st.markdown(f"Price: ${item['price']}")
                st.markdown(f"Brand: {item['brand']}")
                if st.button("Click", key=f"item_id_{item_id}"):
                    update_q(item_id,reward=1)
                    st.session_state.recommendations = recommend_next_top10()
                    st.rerun()