# Brand Reputation & Crisis Monitor (Simple)

This is a minimal working final-project scaffold that analyzes social-media comments for sentiment,
detects spikes in negative sentiment, and suggests simple actions.

## What's included
- `streamlit_app.py` — Streamlit dashboard that:
  - Loads `sample_comments.csv`
  - Runs VADER sentiment analysis
  - Shows sentiment distribution, daily trend, spike detection, top negative comments
  - Outputs suggested actions and allows CSV export

- `sample_comments.csv` — synthetic sample dataset (200 comments over the last 30 days).
- `requirements.txt` — Python dependencies.

## How to run (locally)
1. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate   # macOS / Linux
   venv\Scripts\activate    # Windows
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run Streamlit:
   ```bash
   streamlit run streamlit_app.py
   ```

## Notes
- You can replace `sample_comments.csv` with your own CSV. The app expects columns: `id,timestamp,username,comment,source`
- VADER works best on English text. For other languages, consider multilingual models (HuggingFace) but they require network access.# Brand-Sentiment-Monitor
