# Parts Matcher Pro

Streamlit app using OpenAI v1.x to match parts between two systems by comparing descriptions semantically.

## Features
- Upload Excel or CSV files
- Uses OpenAI Embeddings API (`text-embedding-3-small`)
- Shows top N semantic matches
- Returns CSV export with similarity scores and shared keywords

## Setup

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deployment (Streamlit Cloud)

1. Push this repo to GitHub
2. Go to [streamlit.io/cloud](https://streamlit.io/cloud)
3. Add your OpenAI API key manually at app runtime

## Get an OpenAI API Key

Visit: https://platform.openai.com/account/api-keys
