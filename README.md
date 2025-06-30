# Parts Matcher Pro

Streamlit app to match parts between a catalogue and supplier list using OpenAI semantic similarity.

## Features
- Upload 2 Excel or CSV files
- Matches parts based on description using OpenAI embeddings
- View top N matches and shared keywords
- Export results as CSV
- Includes bin location from supplier file

## Setup

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Streamlit Cloud Deployment

1. Upload these files to a GitHub repo
2. Deploy via [Streamlit Cloud](https://streamlit.io/cloud)
3. Temporarily: Enter your OpenAI API key when prompted in the app

## Get an OpenAI API Key

Visit: https://platform.openai.com/account/api-keys
