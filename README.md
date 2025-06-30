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
2. Go to [streamlit.io/cloud](https://streamlit.io/cloud) and deploy the repo
3. Add your API key in the Secrets section like so:

```toml
OPENAI_API_KEY = "sk-your-openai-key"
```

## Get an OpenAI API Key

Visit: https://platform.openai.com/account/api-keys
