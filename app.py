
import streamlit as st
import pandas as pd
import openai
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import os

st.title("Parts Matcher Pro (with OpenAI Embeddings)")
st.write("Upload two spreadsheets with part descriptions to find likely matches using AI-powered semantic similarity.")

# API Key
openai_api_key = st.text_input("Enter your OpenAI API Key", type="password")

# Upload files
catalogue_file = st.file_uploader("Upload Catalogue File", type=["xlsx", "csv"])
adtrans_file = st.file_uploader("Upload Adtrans File", type=["xlsx", "csv"])

# Similarity threshold input
threshold = st.slider("Description Similarity Threshold", 0.0, 1.0, 0.6, 0.05)
top_n_matches = st.number_input("Top N Matches per Item", min_value=1, max_value=10, value=3)

@st.cache_data(show_spinner=False)
def get_embedding(text, api_key):
    try:
        response = openai.embeddings.create(
            input=text,
            model="text-embedding-3-small",
            api_key=api_key
        )
        return response.data[0].embedding
    except Exception as e:
        st.error(f"Embedding failed: {e}")
        return None

if openai_api_key and catalogue_file and adtrans_file:
    # Load files
    if catalogue_file.name.endswith(".xlsx"):
        df_catalogue = pd.read_excel(catalogue_file)
    else:
        df_catalogue = pd.read_csv(catalogue_file)

    if adtrans_file.name.endswith(".xlsx"):
        df_adtrans = pd.read_excel(adtrans_file)
    else:
        df_adtrans = pd.read_csv(adtrans_file)

    # Preprocess columns
    df_catalogue_clean = df_catalogue.iloc[4:].copy()
    df_catalogue_clean.columns = df_catalogue.iloc[2]
    df_catalogue_subset = df_catalogue_clean[["CPProductNumber", "CPDescription"]].dropna()
    df_catalogue_subset.columns = ["PartNumber", "Description"]

    df_adtrans_subset = df_adtrans[["Part #", "Description"]].dropna()
    df_adtrans_subset.columns = ["PartNumber", "Description"]

    # Bin location map
    adtrans_bin_map = df_adtrans[["Part #", "Location #"]].dropna()
    adtrans_bin_map.columns = ["PartNumber", "BinLocation"]

    # Generate embeddings
    st.info("Generating embeddings for Catalogue descriptions...")
    df_catalogue_subset["Embedding"] = df_catalogue_subset["Description"].apply(lambda x: get_embedding(x, openai_api_key))

    st.info("Generating embeddings for Adtrans descriptions...")
    df_adtrans_subset["Embedding"] = df_adtrans_subset["Description"].apply(lambda x: get_embedding(x, openai_api_key))

    # Prepare matrix
    cat_embeddings = np.array(df_catalogue_subset["Embedding"].tolist())
    ad_embeddings = np.array(df_adtrans_subset["Embedding"].tolist())

    st.info("Calculating similarity scores...")
    similarity_matrix = cosine_similarity(cat_embeddings, ad_embeddings)

    results = []
    for i, row in enumerate(similarity_matrix):
        top_indices = row.argsort()[-top_n_matches:][::-1]
        for j in top_indices:
            score = row[j]
            if score >= threshold:
                desc_1 = df_catalogue_subset.iloc[i]["Description"]
                desc_2 = df_adtrans_subset.iloc[j]["Description"]
                tokens_1 = set(desc_1.lower().split())
                tokens_2 = set(desc_2.lower().split())
                shared = tokens_1.intersection(tokens_2)

                results.append({
                    "Catalogue_PartNumber": df_catalogue_subset.iloc[i]["PartNumber"],
                    "Catalogue_Description": desc_1,
                    "Adtrans_PartNumber": df_adtrans_subset.iloc[j]["PartNumber"],
                    "Adtrans_Description": desc_2,
                    "Description_Similarity": round(score, 3),
                    "Shared_Keyword_Count": len(shared),
                    "Shared_Keywords": ", ".join(shared),
                })

    df_results = pd.DataFrame(results)
    df_results = df_results.merge(
        adtrans_bin_map,
        left_on="Adtrans_PartNumber",
        right_on="PartNumber",
        how="left"
    ).drop(columns=["PartNumber"])

    st.success(f"Found {len(df_results)} matches.")
    st.dataframe(df_results.head(50))

    # Download link
    csv = df_results.to_csv(index=False)
    st.download_button(
        label="Download Results as CSV",
        data=csv,
        file_name="matched_parts_openai.csv",
        mime="text/csv"
    )
